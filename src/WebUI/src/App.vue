<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn icon @click="sidebarOpen = !sidebarOpen">
        <v-icon>mdi-menu</v-icon>
      </v-btn>
      <v-toolbar-title>Fake News Detection</v-toolbar-title>
      <v-spacer />

      <v-btn icon @click="toggleTheme" :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
        <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
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
      <v-container style="height: 100%" fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed } from "vue";
import { useTheme } from "vuetify";

const sidebarOpen = ref(false);

const navItems = [
  { title: "Home", route: "/" },
  { title: "Detector", route: "/detector" },
  { title: "Query Generator", route: "/query-generator" },
];

const theme = useTheme();
const isDark = computed(() => theme.global.name.value === 'dark');

const toggleTheme = () => {
  theme.global.name.value = isDark.value ? 'light' : 'dark';
}
</script>

<style>
.v-btn {
  border-radius: 8px !important;
  text-transform: none !important;
  box-shadow: none;
}

.v-input {
  height: 36px !important;
  .v-field {
    border-radius: 8px !important;
    height: 36px !important;

    .v-field__prepend-inner,
    .v-field__field {
      height: 36px !important;
    }

    .v-field__input {
      height: 36px !important;
      min-height: 36px !important;
      padding: 0 12px !important;
    }
  }
}

.v-card {
  border-radius: 8px !important;
  border: 1px solid rgb(var(--v-theme-on-surface-variant)) !important;
}
</style>
