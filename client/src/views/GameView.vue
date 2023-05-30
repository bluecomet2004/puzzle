<script setup lang="ts">
import { ref } from 'vue';
import { MDBBtn, MDBProgress, MDBProgressBar, MDBIcon } from 'mdb-vue-ui-kit';
import type { PuzzleMatrix } from '@/utils/types';
import GameCard from '@/components/GameCard.vue';
import images from '../utils/images';
import Swal from 'sweetalert2';

const level = 'easy';
const size = 4;
const hints = ref(5);
const totalScore = ref(0);
const rowTemplate = `repeat(${size}, 1fr)`;
const columnTemplate = `repeat(${size}, 1fr)`;
const puzzleMatrix = ref<PuzzleMatrix[]>([]);
const openedCards = ref<PuzzleMatrix[]>([]);
const remainCards = ref(size * size);
const timeLimit: number = 250;
const remainTime = ref(timeLimit);
let imageNumbers: number[] = [];

for (let i = 0; i < size * size / 2; i++) {
  imageNumbers.push(Math.floor(Math.random() * 20));
}

for (let i = 0; i < imageNumbers.length; i++) {
  puzzleMatrix.value.push({
    id: i,
    value: imageNumbers[i],
    open: false,
    matched: false,
    hint: false
  });
  puzzleMatrix.value.push({
    id: i + (size * size / 2),
    value: imageNumbers[i],
    open: false,
    matched: false,
    hint: false
  });
}

for (let i = 0; i < puzzleMatrix.value.length; i++) {
  const j = Math.floor(Math.random() * (i + 1));
  [puzzleMatrix.value[i], puzzleMatrix.value[j]] = [puzzleMatrix.value[j], puzzleMatrix.value[i]];
}

const timer = setInterval(() => {
  remainTime.value--;
  if (remainTime.value <= 0) {
    finishGame();
  }
}, 1000);

function setCardOpen(change: PuzzleMatrix): void {
  for (let i = 0; i < puzzleMatrix.value.length; i++) {
    if (puzzleMatrix.value[i].id === change.id) {
      puzzleMatrix.value[i] = change;

      if (change.open) {
        if (openedCards.value.length >= 1) {
          if (openedCards.value[0].value === change.value) {
            for (let j = 0; j < puzzleMatrix.value.length; j++) {
              if (puzzleMatrix.value[j].id === openedCards.value[0].id) {
                remainCards.value -= 2;
                totalScore.value += 50 / (size * size);

                setTimeout(() => {
                  openedCards.value = [];
                }, 100);

                setTimeout(() => {
                  puzzleMatrix.value[j].matched = true;
                  puzzleMatrix.value[i].matched = true;
                  puzzleMatrix.value[j].open = false;
                  puzzleMatrix.value[i].open = false;

                  if (remainCards.value <= 0) {
                    console.log('Congratulations!');
                  }
                }, 500);
              }
            }
          } else {
            for (let j = 0; j < puzzleMatrix.value.length; j++) {
              if (puzzleMatrix.value[j].id === openedCards.value[0].id) {
                setTimeout(() => {
                  openedCards.value = [];
                });

                setTimeout(() => {
                  puzzleMatrix.value[j].open = false;
                  puzzleMatrix.value[i].open = false;
                }, 1000);
              }
            }
          }
        } else {
          openedCards.value.push(change);
        }
      } else {
        openedCards.value.pop();
      }
    }
  }
}

function getHint(): void {
  Swal.fire({
    title: "Need a help?",
    icon: 'question',
    text: "You will lose your score by -0.5 star.",
    confirmButtonText: 'Yes',
    showDenyButton: true
  }).then(() => {
    for (let i = 0, j = puzzleMatrix.value.length - 1; i < j; i++, j--) {
      if (!puzzleMatrix.value[i].matched && !puzzleMatrix.value[j].matched && puzzleMatrix.value[i].value === puzzleMatrix.value[j].value) {
        puzzleMatrix.value[i].hint = true;
        puzzleMatrix.value[j].hint = true;
        hints.value--;
        totalScore.value -= 0.5;
        break;
      }
    }
  });
}

function finishGame() {
  clearInterval(timer);

  if (totalScore.value < 0) {
    totalScore.value = 0;
  } else {
    totalScore.value = Math.ceil(totalScore.value) / 10;
  }
  const spentHour = Math.floor((timeLimit-remainTime.value) / 60);
  const spentSecond = timeLimit - remainTime.value;

  Swal.fire({
    title: "Game Over",
    icon: 'info',
    html: `Your Score: ${totalScore.value}<br />Spent Time: ${spentHour>9?spentHour:`0${spentHour}`}:${spentSecond>9?spentSecond:`0${spentSecond}`}`
  });
}

function confirmFinish() {
  Swal.fire({
    title: "Finish Game",
    icon: 'question',
    text: "Are you sure you want to over?",
    showDenyButton: true
  }).then(finishGame);
}
</script>

<template>
  <div class="center-align">
    <RouterLink to="/" style="position: absolute;top: 0;left: 0;margin: 24px;">
      BACK
    </RouterLink>

    <div class="board">
      <h1>LEVEL: {{ level.toUpperCase() }}</h1>

      <MDBProgress>
        <MDBProgressBar :value="remainTime / timeLimit * 100" />
      </MDBProgress>
      <p>Time: {{ remainTime / 60 > 9 ? Math.floor(remainTime / 60) : `0${Math.floor(remainTime / 60)}` }}:{{ remainTime %
        60 >
        9 ? remainTime % 60 : `0${remainTime % 60}` }}</p>

      <div>
        <MDBBtn title="Hint" color="success" floating v-for="n in hints" :key="n" @click="getHint">
          <MDBIcon icon-style="fab" icon="medapps" size="lg" />
        </MDBBtn>
      </div>

      <br />

      <MDBBtn color="primary" size="lg" style="width: 150px" @click="confirmFinish">
        FINISH
      </MDBBtn>
    </div>
    <div class="playground" :style="`grid-template-rows: ${rowTemplate}; grid-template-columns: ${columnTemplate}`">
      <GameCard v-for="(matrix, index) in puzzleMatrix" :key="index" :data="matrix"
        @change="(change) => setCardOpen(change)">
        <img :src="images[matrix.value]" />
      </GameCard>
    </div>
  </div>
</template>