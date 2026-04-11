<script setup>
import { NMenu } from "naive-ui";
import { h, ref } from "vue";

function renderIcon(icon) {
  return () => h(NIcon, null, { default: () => h(icon) });
}

const menuOptions = [
  {
    label: () => h(
      "a",
      {
        href: "/login"
      },
      "Войти"
    ),
    key: "hear-the-wind-sing"
  }
]

const activeKey = ref(null);
</script>

<template>
  <n-menu
        v-model:value="activeKey"
        mode="horizontal"
        :options="menuOptions"
        responsive
      />
  <router-view />
</template>

<style scoped>

</style>
