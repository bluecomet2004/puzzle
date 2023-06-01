import router from "@/router";
import type { GameHistory } from "@/utils/types";
import axios from "axios";
import { defineStore } from "pinia";
import Swal from "sweetalert2";
import { ref } from "vue";

export const useGameStore = defineStore('game', () => {
  const options = ref({
    difficulty: "easy",
    size: 4,
    disabled: true,
    totalTime: 300,
    setted: false
  });

  const result = ref({
    score: 0,
    overTime: 0
  });

  function reportHistory(data: GameHistory) {
    return axios.post('http://127.0.0.1:8000/api/history/', data)
      .then(({data}) => {
        result.value.score = data.history.score;
        result.value.overTime = data.history.overTime;
        router.push('/result');
      })
      .catch(() => {
        Swal.fire({
          title: "Server Error",
          icon: "error",
          text: "There goes some error. Please try again."
        })
        .then(() => router.push('/auth'));
      })
  }

  return { options, result, reportHistory }
})