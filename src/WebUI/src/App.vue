<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn icon @click="sidebarOpen = !sidebarOpen">
        <v-icon>mdi-menu</v-icon>
      </v-btn>
      <v-toolbar-title>Fake News Detection</v-toolbar-title>
    </v-app-bar>

    <v-navigation-drawer app v-model="sidebarOpen" width="250">
      <v-list dense>
        <v-list-item
          v-for="item in navItems"
          :key="item.title"
          :to="item.route"
          link
        >
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container style="height: 100%;" fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from "vue";

const sidebarOpen = ref(false);

const navItems = [
  { title: "Home", route: "/" },
  { title: "Detector", route: "/detector" },
  { title: "Query Generator", route: "/query-generator" },
];
</script>

<style scoped></style>
