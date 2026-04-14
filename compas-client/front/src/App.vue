<script setup>
import { NMenu, NIcon } from "naive-ui"; 
import { h, ref } from "vue";
import { BookOutline as BookIcon } from "@vicons/ionicons5"; 

function renderIcon(icon) {
  return () => h(NIcon, null, { default: () => h(icon) });
}

const COLOR_NORMAL = '#ffffff';
const COLOR_HOVER = '#00B1FF';

const menuOptions = [
  {
    label: () => h(
      "a",
      {
        href: "/login",
        style: {
          color: COLOR_NORMAL,
          textDecoration: 'none',
          display: 'block',
          width: '100%',
          height: '100%',
          transition: 'color 0.3s'
        },
        onMouseover: (e) => {
          e.target.style.color = COLOR_HOVER;
          
        },
        onMouseout: (e) => {
          e.target.style.color = COLOR_NORMAL;
        }
      },
      "Войти"
    ),
    key: "login",
  }
]

const activeKey = ref(null);
</script>

<template>
  <n-menu
    class="custom-menu"
    v-model:value="activeKey"
    mode="horizontal"
    :options="menuOptions"
    responsive
  />
  <router-view />
</template>

<style>
</style>