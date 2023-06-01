<script setup lang="ts">
import Swal from 'sweetalert2';
import { MDBInput, MDBRadio, MDBBtn, MDBIcon, MDBRange } from 'mdb-vue-ui-kit';
import { useGameStore } from '../stores/game';
import router from '@/router';

const store = useGameStore();

const changeLevel = (value: string) => {
  store.options.difficulty = value;

  switch(value) {
    case 'easy': store.options.size = 4; store.options.disabled = true; break;
    case 'medium': store.options.size = 6; store.options.disabled = true; break;
    case 'hard': store.options.size = 10; store.options.disabled = true; break;
    case 'custom': store.options.disabled = false; break;
    default: break;
  }
}

const setOption = () => {
  if(store.options.size % 2 !== 0) {
    Swal.fire({
      toast: true,
      position: "top-right",
      icon: 'error',
      timer: 3000,
      timerProgressBar: true,
      text: "Matrix must be made by even numbers.",
      showConfirmButton: false
    });
  } else if(store.options.size < 4) {
    Swal.fire({
      toast: true,
      position: "top-right",
      icon: 'error',
      timer: 3000,
      timerProgressBar: true,
      text: "Matrix must be grater than 4.",
      showConfirmButton: false
    });
  } else if(store.options.size > 20) {
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
    store.options.setted = true;
    router.push("/stage");
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
            v-model="store.options.difficulty"
          />
          <MDBRadio
            label="Medium"
            value="medium"
            @input="changeLevel('medium')"
            v-model="store.options.difficulty"
          />
          <MDBRadio
            label="Hard"
            value="hard"
            @input="changeLevel('hard')"
            v-model="store.options.difficulty"
          />
          <MDBRadio
            label="Custom"
            value="custom"
            @input="changeLevel('custom')"
            v-model="store.options.difficulty"
          />
        </div>

        <div class="g-col-6">
          <MDBInput
            type="number"
            size="lg"
            max=12
            min=4
            step=2
            v-model="store.options.size"
            :disabled="store.options.disabled"
            />
          &nbsp;&nbsp;X&nbsp;&nbsp;
          <MDBInput
            type="number"
            size="lg"
            max=12
            min=4
            step=2
            v-model="store.options.size"
            :disabled="store.options.disabled"
          />
        </div>
      </div>

      <div style="margin-top:32px">
        <p><MDBIcon icon="home" /> Time(second):</p>
        <MDBRange :min="0" :max="2000" v-model="store.options.totalTime" />
      </div>

      <div class="content-center">
        <MDBBtn color="primary" @click="setOption">OK</MDBBtn>
      </div>
    </div>
  </div>
</template>