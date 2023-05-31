import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useUserStore = defineStore('user', () => {
  const userData = ref({
    name: '',
    email: '',
    password: ''
  });

  function registerUser(user: any) {
    userData.value = {
      ...userData.value,
      name: user.name,
      email: user.email,
      password: user.password
    }

    return axios.post('http://127.0.0.1:8000/api/users/', userData.value)
      .then(res => {
        return res.data;
      })
      .catch(({response:{data}}) => {
        return data;
      });
  }

  return { userData, registerUser }
});