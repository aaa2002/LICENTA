<template>
  <v-container class="qGen-page-wrapper">
    <div><h1>Query Generator</h1></div>
    <v-row>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Google Query</v-card-title>
          <v-card-text
            class="d-flex align-center justify-space-between"
            style="word-break: break-word"
          >
            <div style="flex: 1; margin-right: 16px">
              {{ apiResponse.google }}
            </div>
            <div class="d-flex">
              <v-btn icon @click="copyToClipboard(apiResponse.google)">
                <v-icon>mdi-content-copy</v-icon>
              </v-btn>
              <v-btn icon @click="openInGoogle(apiResponse.google)">
                <v-icon>mdi-web</v-icon>
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Bing Query</v-card-title>
          <v-card-text
            class="d-flex align-center justify-space-between"
            style="word-break: break-word"
          >
            <div style="flex: 1; margin-right: 16px">
              {{ apiResponse.bing }}
            </div>
            <div class="d-flex">
              <v-btn icon @click="copyToClipboard(apiResponse.bing)">
                <v-icon>mdi-content-copy</v-icon>
              </v-btn>
              <v-btn icon @click="openInBing(apiResponse.bing)">
                <v-icon>mdi-web</v-icon>
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>DuckDuckGo Query</v-card-title>
          <v-card-text
            class="d-flex align-center justify-space-between"
            style="word-break: break-word"
          >
            <div style="flex: 1; margin-right: 16px">
              {{ apiResponse.duckduckgo }}
            </div>
            <div class="d-flex">
              <v-btn icon @click="copyToClipboard(apiResponse.duckduckgo)">
                <v-icon>mdi-content-copy</v-icon>
              </v-btn>
              <v-btn icon @click="openInDuckDuckGo(apiResponse.duckduckgo)">
                <v-icon>mdi-web</v-icon>
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <!-- <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Detector Card 4</v-card-title>
          <v-card-text>
            This is the content of the fourth detector card.
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Detector Card 5</v-card-title>
          <v-card-text>
            This is the content of the fifth detector card.
          </v-card-text>
        </v-card>
      </v-col> -->
    </v-row>

    <!-- <v-row>
      <div v-if="isLoading" class="loading-indicator">
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </div>
      <v-card class="main-response-card" v-else>
        <v-card-title>Results</v-card-title>
        <v-card-text> </v-card-text>
      </v-card>
    </v-row> -->

    <v-row class="user-input-row" fluid>
      <v-text-field
        v-model="userInput"
        label="Enter text"
        variant="outlined"
        clearable
        prepend-inner-icon="mdi-magnify"
        class="user-input-field"
      >
      </v-text-field>
      <v-btn
        color="primary"
        @click="getResult"
        class="ml-2"
        :disabled="isLoading"
      >
        Check
      </v-btn>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import {
  copyToClipboard,
  openInGoogle,
  openInBing,
  openInDuckDuckGo,
} from "../helpers/functions";

const apiResponse = ref({
  google: "",
  bing: "",
  duckduckgo: "",
});
const userInput = ref("");
const isLoading = ref(false);

const getResult = () => {
  isLoading.value = true;
  axios
    .post("http://localhost:8000/generate-query", {
      text: userInput.value,
    })
    .then((response) => {
      apiResponse.value = response.data;
      isLoading.value = false;
    })
    .catch((error) => {
      console.error("There was an error!", error);
      apiResponse.value = "Error: " + error.message;
      isLoading.value = false;
    });
};
</script>

<style>
.qGen-page-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.qGen-page-wrapper .user-input-field .v-input__details {
  display: none !important;
}

.qGen-page-wrapper .user-input-row {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  height: 64px !important;
  max-height: 64px !important;
}

.main-response-card {
  margin-top: 20px;
  width: 100%;
}
</style>
