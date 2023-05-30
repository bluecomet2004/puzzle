<script setup lang="ts">
import Swal from 'sweetalert2';
import { reactive } from 'vue';
import { MDBInput } from 'mdb-vue-ui-kit';
import * as yup from 'yup';

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
  confirm: ''
});

const loginSchema = yup.object().shape({
  password: yup.string().required(),
  email: yup.string().required().email()
});

const registerSchema = yup.object().shape({
  confirm: yup.string().required().oneOf([yup.ref('password')], "Passwords must be match."),
  password: yup.string().required().min(6).max(30),
  email: yup.string().required().email(),
  name: yup.string().required().max(255)
});

const loginSubmit = () => {
  loginSchema.validate(loginData)
    .then(() => console.info('Validation success!'))
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
    .then(() => console.info('Validation success!'))
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
  <RouterLink
    to="/"
    style="
      position: absolute;
      top: 0;
      left: 0;
      margin: 24px;
    "
  >
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
          <MDBInput name="confirm" size="lg" type="password" label="Confirm Password" v-model="registerData.confirm" />

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