<script setup lang="ts">
import { MDBBtn } from 'mdb-vue-ui-kit';
import { useUserStore } from '../stores/user';
import router from '@/router';

const store = useUserStore();
let token = localStorage.getItem('access_token');

function login() {
  if(token) {
    localStorage.removeItem('access_token');
    token = localStorage.getItem('access_token');
  } else {
    router.push("/auth");
  }
}

function startGame() {
  store.accessToken();
}
</script>

<template>
  <div class="center-align" style="flex-direction: column;">
    <h1 class="title">PUZZLE</h1>
    <p class="subtitle">Version: 1.0</p>

    <MDBBtn
      color="success"
      style="font-size:4vmin;
        font-weight: bold;
        width: 32vmin;
        height: 8vmin;
        min-height: 45px;
        margin-bottom: 12px;
        transform: scale(0);
        animation: popup_anim .4s .5s forwards"
      @click="login"
    >
      {{ token ? "LOGOUT" : "LOGIN" }}
    </MDBBtn>

    <MDBBtn
      color="primary"
      style="font-size:4vmin;
        font-weight: bold;
        width: 32vmin;
        height: 8vmin;
        min-height: 45px;
        transform: scale(0);
        animation: popup_anim .4s .75s forwards"
      @click="startGame"
      >
      START
    </MDBBtn>
  </div>
</template>