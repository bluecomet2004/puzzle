<script setup lang="ts">
import Swal from 'sweetalert2';
import { MDBInput, MDBRadio, MDBBtn, MDBIcon, MDBRange } from 'mdb-vue-ui-kit';
import { reactive } from 'vue';

const level = reactive({
  difficulty: 'easy',
  size: 4,
  disabled: true,
  time: 300
});

const changeLevel = (value: string) => {
  level.difficulty = value;

  switch(value) {
    case 'easy': level.size = 4; level.disabled = true; break;
    case 'medium': level.size = 6; level.disabled = true; break;
    case 'hard': level.size = 10; level.disabled = true; break;
    case 'custom': level.disabled = false; break;
    default: break;
  }
}

const sendOption = () => {
  if(level.size % 2 !== 0) {
    Swal.fire({
      toast: true,
      position: "top-right",
      icon: 'error',
      timer: 3000,
      timerProgressBar: true,
      text: "Matrix must be made by even numbers.",
      showConfirmButton: false
    });
  } else if(level.size < 4) {
    Swal.fire({
      toast: true,
      position: "top-right",
      icon: 'error',
      timer: 3000,
      timerProgressBar: true,
      text: "Matrix must be grater than 4.",
      showConfirmButton: false
    });
  } else if(level.size > 20) {
    Swal.fire({
      toast: true,
      position: "top-right",
      icon: 'error',
      timer: 3000,
      timerProgressBar: true,
      text: "Matrix must be less than 20",
      showConfirmButton: false
    });
  } else {
    window.alert('Success');
  }
}
</script>

<template>
  <div class="center-align">
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

    <div class="option-modal">
      <h1>OPTION</h1>

      <div class="grid">
        <div class="g-col-6">
          <MDBRadio
            label="Easy"
            value="easy"
            @input="changeLevel('easy')"
            v-model="level.difficulty"
          />
          <MDBRadio
            label="Medium"
            value="medium"
            @input="changeLevel('medium')"
            v-model="level.difficulty"
          />
          <MDBRadio
            label="Hard"
            value="hard"
            @input="changeLevel('hard')"
            v-model="level.difficulty"
          />
          <MDBRadio
            label="Custom"
            value="custom"
            @input="changeLevel('custom')"
            v-model="level.difficulty"
          />
        </div>

        <div class="g-col-6">
          <MDBInput
            type="number"
            size="lg"
            max=12
            min=4
            step=2
            v-model="level.size"
            :disabled="level.disabled"
            />
          &nbsp;&nbsp;X&nbsp;&nbsp;
          <MDBInput
            type="number"
            size="lg"
            max=12
            min=4
            step=2
            v-model="level.size"
            :disabled="level.disabled"
          />
        </div>
      </div>

      <div style="margin-top:32px">
        <p><MDBIcon icon="home" /> Time(second):</p>
        <MDBRange :min="0" :max="3600" v-model="level.time" />
      </div>

      <div class="content-center">
        <MDBBtn color="primary" @click="sendOption">OK</MDBBtn>
      </div>
    </div>
  </div>
</template>