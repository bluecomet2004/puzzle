<script setup lang="ts">
import Swal from 'sweetalert2';
import { useUserStore } from '@/stores/user';
import { reactive } from 'vue';
import { MDBInput } from 'mdb-vue-ui-kit';
import * as yup from 'yup';

const store = useUserStore();

const authMethod = reactive({
  isLogin: true
});

const loginData = reactive({
  email: '',
  password: ''
});

const registerData = reactive({
  name: '',
  email: '',
  password: '',
  password2: ''
});

const loginSchema = yup.object().shape({
  password: yup.string().required(),
  email: yup.string().required().email()
});

const registerSchema = yup.object().shape({
  password2: yup.string().required().oneOf([yup.ref('password')], "Passwords must be match."),
  password: yup.string().required().min(6).max(30),
  email: yup.string().required().email(),
  name: yup.string().required().max(255)
});

const loginSubmit = () => {
  loginSchema.validate(loginData)
    .then(() => {
      store.loginUser(loginData)
        .then(response => {
          if(response.success === true) {
            Swal.fire({
              title: response.message,
              icon: 'success',
              confirmButtonText: "Go to option"
            })
            .then(() => {
              localStorage.setItem('access_token', response.token);
              store.accessToken();
            });
          } else {
            Swal.fire({
              toast: true,
              position: 'top-right',
              icon: 'error',
              timer: 3000,
              timerProgressBar: true,
              text: response.message,
              showConfirmButton: false
            });
          }
        })
    })
    .catch(error => Swal.fire({
      toast: true,
      position: "top-right",
      timer: 3000,
      timerProgressBar: true,
      icon: "error",
      text: error,
      showConfirmButton: false
    }));
}

const registerSubmit = () => {
  registerSchema.validate(registerData)
    .then(() => {
      store.registerUser(registerData)
        .then(response => {
          if (response.success) {
            Swal.fire({
              toast: true,
              position: 'top-right',
              icon: 'success',
              timer: 3000,
              timerProgressBar: true,
              text: response.message,
              showConfirmButton: false
            });

            registerData.name = '';
            registerData.email = '';
            registerData.password = '';
            registerData.password2 = '';
            authMethod.isLogin = true;
          } else {
            Swal.fire({
              toast: true,
              position: 'top-right',
              icon: 'error',
              timer: 3000,
              timerProgressBar: true,
              text: response.message,
              showConfirmButton: false
            });
          }
        })
        .catch(error => Swal.fire({
          toast: true,
          position: 'top-right',
          icon: 'error',
          timer: 3000,
          timerProgressBar: true,
          text: error.message,
          showConfirmButton: false
        }));
    })
    .catch(error => Swal.fire({
      toast: true,
      position: "top-right",
      timer: 3000,
      timerProgressBar: true,
      icon: "error",
      text: error,
      showConfirmButton: false
    }));
}

const toggleMethod = () => {
  authMethod.isLogin = !authMethod.isLogin;
}
</script>

<template>
  <RouterLink to="/" style="
        position: absolute;
        top: 0;
        left: 0;
        margin: 24px;
      ">
    BACK
  </RouterLink>

  <div class="center-align">
    <div class="auth-card">
      <div class="login">
        <form :class="authMethod.isLogin ? '' : 'invisible'" @submit.prevent="loginSubmit">
          <MDBInput name="email" label="Email ID" type="text" size="lg" v-model="loginData.email" />
          <MDBInput name="password" label="Password" type="password" size="lg" v-model="loginData.password" />

          <p @click="toggleMethod">You don't have an account?</p>
          <button>LOGIN</button>
        </form>
      </div>

      <div class="register">
        <form :class="!authMethod.isLogin ? '' : 'invisible'" @submit.prevent="registerSubmit">
          <MDBInput name="name" size="lg" type="text" label="Full Name" v-model="registerData.name" />
          <MDBInput name="email" size="lg" type="text" label="Email ID" v-model="registerData.email" />
          <MDBInput name="password" size="lg" type="password" label="New Password" v-model="registerData.password" />
          <MDBInput name="password2" size="lg" type="password" label="Confirm Password" v-model="registerData.password2" />

          <p @click="toggleMethod">Already have an account?</p>
          <button>REGISTER</button>
        </form>
      </div>

      <span :class="authMethod.isLogin ? 'cover-panel' : 'cover-panel active'">
        <h1 v-if="authMethod.isLogin">LOGIN</h1>
        <h1 v-else>REGISTER</h1>
      </span>
    </div>
  </div>
</template>

<style></style>