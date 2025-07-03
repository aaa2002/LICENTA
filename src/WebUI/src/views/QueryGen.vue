<template>
  <v-container class="qGen-page-wrapper">
    <div class="mb-4"><h1>Query Generator</h1></div>
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
              <v-btn
                icon
                class="mr-1"
                @click="copyToClipboard(apiResponse.google)"
              >
                <v-icon size="x-small">mdi-content-copy</v-icon>
              </v-btn>
              <v-btn icon @click="openInGoogle(apiResponse.google)">
                <v-icon size="x-small">mdi-web</v-icon>
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
              <v-btn
                class="mr-1"
                icon
                @click="copyToClipboard(apiResponse.bing)"
              >
                <v-icon size="x-small">mdi-content-copy</v-icon>
              </v-btn>
              <v-btn icon @click="openInBing(apiResponse.bing)">
                <v-icon size="x-small">mdi-web</v-icon>
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
              <v-btn
                icon
                class="mr-1"
                @click="copyToClipboard(apiResponse.duckduckgo)"
              >
                <v-icon size="x-small">mdi-content-copy</v-icon>
              </v-btn>
              <v-btn icon @click="openInDuckDuckGo(apiResponse.duckduckgo)">
                <v-icon size="x-small">mdi-web</v-icon>
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Web Result Recommendations</v-card-title>
          <v-card-subtitle
            >For further reading, on the topic: {{ userInput }}</v-card-subtitle
          >
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="(item, index) in recommendations"
                class="mb-2"
                :key="index"
              >
                <v-list-item-content>
                  <v-list-item-title class="font-weight-bold text-lg mb-1">
                    <a :href="item.href" target="_blank">
                      {{ item.title }}
                    </a>
                  </v-list-item-title>
                  <v-list-item-subtitle> <span v-html="item.body"></span></v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Article Recommendations</v-card-title>
          <v-card-subtitle>
            For further reading, on the topic: {{ userInput }}
          </v-card-subtitle>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="(article, index) in articles"
                :key="index"
                class="mb-4"
              >
                <v-list-item-content>
                  <v-list-item-title class="font-weight-bold text-lg mb-1">
                    <a
                      :href="article.url.replace('abs', 'pdf')"
                      target="_blank"
                    >
                      {{ article.title }}
                    </a>
                  </v-list-item-title>

                  <v-list-item-subtitle class="text-body-2 mb-1">
                    <strong>Authors:</strong> {{ article.authors.join(", ") }}
                  </v-list-item-subtitle>

                  <v-list-item-subtitle class="text-body-2">
                    <strong>Abstract:</strong> {{ article.abstract }}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
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
const recommendations = ref([]);
const articles = ref([]);

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

  axios
    .post("http://localhost:8000/get-recommendations", {
      inputText: userInput.value,
    })
    .then((response) => {
      recommendations.value = response.data.results;
    })
    .catch((error) => {
      console.error("There was an error fetching recommendations!", error);
    });

  axios
    .post("http://localhost:8000/get-articles", {
      inputText: userInput.value,
    })
    .then((response) => {
      articles.value = response.data.results;
    })
    .catch((error) => {
      console.error("There was an error fetching articles!", error);
    });
};
</script>

<style>
.qGen-page-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;

  .v-btn--icon {
    width: 24px !important;
    height: 24px !important;
    min-width: 24px !important;
    min-height: 24px !important;
    padding: 0;
    border-radius: 8px;
    box-shadow: none !important;
    border: 1px solid rgb(var(--v-theme-on-surface-variant)) !important;
  }
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
