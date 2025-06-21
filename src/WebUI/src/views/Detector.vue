<template>
  <v-container class="detector-page-wrapper">
    <div><h1>Detector</h1></div>

    <v-row>
      <div v-if="isLoading" class="loading-indicator mt-4">
        <v-skeleton-loader
          type="article"
          :elevation="1"
          loading
        ></v-skeleton-loader>
      </div>
      <v-card class="main-response-card" v-else>
        <v-card-title>Detector Result</v-card-title>
        <v-card-text>
          <div v-if="apiResponse">
            <div class="d-flex">
              <div
                class="icon-wrapper mr-2"
                :class="
                  apiResponse.final_label === 'real'
                    ? 'icon-wrapper--success'
                    : 'icon-wrapper--error'
                "
              >
                <v-icon
                  :color="
                    apiResponse.final_label === 'real' ? 'success' : 'error'
                  "
                  size="44"
                  >{{
                    apiResponse.final_label === "real"
                      ? "mdi-check-circle"
                      : "mdi-alert-circle"
                  }}</v-icon
                >
              </div>
              <div class="d-flex flex-column">
                <span
                  ><strong>Score:</strong>
                  {{ formatToPercentage(apiResponse.score) }}</span
                >
                <RealFalseChip :label="apiResponse.final_label"></RealFalseChip>
              </div>
            </div>
            <v-expansion-panels class="mt-4">
              <v-expansion-panel>
                <v-expansion-panel-title> Details </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <div
                    v-for="(detail, key) in apiResponse.details"
                    :key="key"
                    class="mb-4"
                  >
                    <div v-if="!ignoredKeys.includes(key)">
                      <h3 class="mb-2">{{ agentNameMap[key] }}</h3>
                      <p class="d-flex align-center mb-2">
                        <RealFalseChip :label="detail.label"></RealFalseChip>
                      </p>
                      <p>
                        <strong>Confidence:</strong>
                        {{ formatToPercentage(detail.confidence) }}
                      </p>
                      <p v-if="detail.explanation">
                        <strong>Explanation:</strong> {{ detail.explanation }}
                      </p>
                      <p v-if="detail.overlap_score">
                        <strong>Overlap Score:</strong>
                        {{ detail.overlap_score }}
                      </p>
                      <p
                        v-if="detail.search_terms && detail.search_terms.length"
                      >
                        <strong>Search Terms:</strong>
                        {{ detail.search_terms.join(", ") }}
                      </p>
                    </div>
                    <v-divider
                      class="mt-4"
                      v-if="
                        !ignoredKeys.includes(key) && key !== 'coherence_result'
                      "
                    ></v-divider>
                  </div>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
          <div v-else>No result available.</div>
        </v-card-text>
      </v-card>
    </v-row>

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
import RealFalseChip from "../components/RealFalseChip.vue";

const apiResponse = ref("");
const userInput = ref("");
const isLoading = ref(false);

const agentNameMap = {
  fn_result: "Fake News Detector",
  coherence_result: "Coherence Checker",
  wiki_result: "Wikipedia Search",
  scraper_result: "Web Scraper",
};

const ignoredKeys = ["input", "search_results", "web_text"];

const formatToPercentage = (value) => {
  if (typeof value === "number") {
    return (value * 100).toFixed(2) + "%";
  }
  return value;
};

const getResult = () => {
  isLoading.value = true;
  axios
    .post("http://localhost:8000/predict", {
      text: userInput.value,
    })
    .then((response) => {
      console.log("Response from API:", response.data);
      apiResponse.value = response.data;
      isLoading.value = false;
    })
    .catch((error) => {
      console.error("There was an error!", error);
      apiResponse.value = "Error: " + error.message;
      isLoading.value = false;
    });
};

const responseExample = ref({
  final_label: "real",
  score: 0.585,
  details: {
    input: "Doanld Trump is the 45th president of the United states",
    search_results: [
      "45th & 47th President of the United States. ... President Donald J. Trump is returning to the White House to build upon his previous successes and use his mandate to reject the extremist policies ... Donald J. Trump Sworn In as the 47th President of the United States January 20, 2025. ... President Donald J. Trump Addresses the West Point Class of 2025 May 25, 2025 WASHINGTON (AP) — Donald Trump was elected the 47th president of the United States on Wednesday, an extraordinary comeback for a former president who refused to accept defeat four years ago ... Donald John Trump (born June 14, 1946) is an American politician, media personality, and businessman who is the 47th president of the United States. A member of the Republican Party, he served as the 45th president from 2017 to 2021. Donald Trump, who overcame impeachments, criminal indictments and a pair of assassination attempts to win another term in the White House, was sworn in Monday as the 47th U.S. president taking ... WASHINGTON − Donald Trump was sworn in Monday as the 47th president of the United States, returning to the White House after overcoming four criminal indictments and two assassination attempts ... Donald Trump was sworn in as the 47th president of the United States in the Rotunda of the U.S. Capitol at noon on Monday, beginning his second term as he returns to the White House after four years. WASHINGTON (7News) — Donald Trump was sworn in as the 47th president of the United States on Monday, alongside J.D. Vance as the next vice president. Due to winter weather, the ceremony took ... Trump has done it again. ... Donald Trump is elected 47th president of the United States in a stunning return to power. ... Donald Trump elected 47th president of the United States. Donald Trump was elected the 47th President of the United States on Wednesday, after the AP called Wisconsin and the election for the former president, ensuring a stunning political comeback and a ...",
    ],
    web_text:
      "45th & 47th President of the United States. ... President Donald J. Trump is returning to the White House to build upon his previous successes and use his mandate to reject the extremist policies ... Donald J. Trump Sworn In as the 47th President of the United States January 20, 2025. ... President Donald J. Trump Addresses the West Point Class of 2025 May 25, 2025 WASHINGTON (AP) — Donald Trump was elected the 47th president of the United States on Wednesday, an extraordinary comeback for a former president who refused to accept defeat four years ago ... Donald John Trump (born June 14, 1946) is an American politician, media personality, and businessman who is the 47th president of the United States. A member of the Republican Party, he served as the 45th president from 2017 to 2021. Donald Trump, who overcame impeachments, criminal indictments and a pair of assassination attempts to win another term in the White House, was sworn in Monday as the 47th U.S. president taking ... WASHINGTON − Donald Trump was sworn in Monday as the 47th president of the United States, returning to the White House after overcoming four criminal indictments and two assassination attempts ... Donald Trump was sworn in as the 47th president of the United States in the Rotunda of the U.S. Capitol at noon on Monday, beginning his second term as he returns to the White House after four years. WASHINGTON (7News) — Donald Trump was sworn in as the 47th president of the United States on Monday, alongside J.D. Vance as the next vice president. Due to winter weather, the ceremony took ... Trump has done it again. ... Donald Trump is elected 47th president of the United States in a stunning return to power. ... Donald Trump elected 47th president of the United States. Donald Trump was elected the 47th President of the United States on Wednesday, after the AP called Wisconsin and the election for the former president, ensuring a stunning political comeback and a ...",
    fn_result: {
      label: "fake",
      confidence: 0.5755769725846482,
      probabilities: {
        fake: 0.5755769725846482,
        real: 0.42442302741535176,
      },
    },
    wiki_result: {
      label: "real",
      confidence: 0.2,
      overlap_score: 0.8,
      search_terms: [
        "Trump",
        "Doanld Trump",
        "President",
        "The United States",
        "The 45Th President",
      ],
    },
    scraper_result: {
      label: "real",
      confidence: 0.9,
      explanation:
        "The claim matches the extracted knowledge, as Donald Trump is indeed the 45th President of the United States.",
    },
    coherence_result: {
      label: "real",
      confidence: 1,
      explanation:
        "The paragraph contains a statement that appears to be a factual assertion, which is coherent and makes sense.",
    },
  },
});
</script>

<style>
.detector-page-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.detector-page-wrapper .user-input-field .v-input__details {
  display: none !important;
}

.detector-page-wrapper .user-input-row {
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

.icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 8px;
}

.icon-wrapper--success {
  background-color: rgb(var(--v-theme-success-lighten-3)) !important;
}

.icon-wrapper--error {
  background-color: rgb(var(--v-theme-error-lighten-3)) !important;
}

.loading-indicator {
  width: 100% !important;
  height: 100% !important;
}
</style>
