import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/HomeView.vue';
import Auth from '@/views/AuthView.vue';
import Game from '@/views/GameView.vue';
import Option from '@/views/OptionView.vue';
import Result from '@/views/ResultView.vue';
import NotFound from '@/views/NotFound.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home
    },
    {
      path: "/auth",
      name: "Auth",
      component: Auth
    },
    {
      path: "/option",
      name: "Option",
      component: Option
    },
    {
      path: "/stage",
      name: "Game",
      component: Game
    },
    {
      path: "/result",
      component: Result
    },
    {
      path: "/:pathMatch(.*)*",
      name: "NotFound",
      component: NotFound
    }
  ]
})

export default router
