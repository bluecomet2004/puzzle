<script setup lang="ts">
import { MDBBtn } from 'mdb-vue-ui-kit';

function login() {
  window.location.href = '/auth';
}

function startGame() {
  window.location.href = '/option';
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
      LOGIN
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