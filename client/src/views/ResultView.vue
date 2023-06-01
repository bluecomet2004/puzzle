<script setup lang="ts">
import { MDBIcon } from 'mdb-vue-ui-kit';
import { useGameStore } from '../stores/game';
import JSConfetti from 'js-confetti';


const store = useGameStore();
const confetti = new JSConfetti();
let score = store.result.score;
let time = store.result.overTime;
let star_icons: Array<string> = [];

if(!store.options.setted) window.location.href = "/option";

while(score > 0) {
  if(score < 1) {
    star_icons.push('star-half');
  } else {
    star_icons.push('star');
  }
  score--;
}

if(store.result.score === 5) {
  confetti.addConfetti();
}

const spentHour = Math.floor(time / 60);
const spentSecond = time % 60;
</script>

<template>
  <div class="center-align">
    <div class="result-card">
      <h1>RESULT</h1>

      <div>
        <MDBIcon v-for="(icon,index) in star_icons" :key="index" :icon="icon" style="font-size: 10vmin; color:orange" />
      </div>

      <p>
        <b v-if="store.result.score === 5" style="color:red">Congatulations!</b>
        You've got {{ store.result.score }}
        <br />
        Taken Time: {{ spentHour>9?spentHour:`0${spentHour}` }} : {{ spentSecond>9?spentSecond:`0${spentSecond}` }}
      </p>

      <RouterLink to="/">Go to Home</RouterLink>
    </div>
  </div>
</template>