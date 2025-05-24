<template>
  <v-container class="detector-page-wrapper">
    <div><h1>Detector</h1></div>
    <!-- <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Detector Card 1</v-card-title>
          <v-card-text>
            This is the content of the first detector card.
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Detector Card 2</v-card-title>
          <v-card-text>
            This is the content of the second detector card.
          </v-card-text>
        </v-card>
      </v-col>
        <v-col cols="12" md="6">
            <v-card>
            <v-card-title>Detector Card 3</v-card-title>
            <v-card-text>
                This is the content of the third detector card.
            </v-card-text>
            </v-card>
        </v-col>
        <v-col cols="12" md="6">
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
        </v-col>
        <v-col cols="12" md="6">
            <v-card>
            <v-card-title>Detector Card 6</v-card-title>
            <v-card-text>
                This is the content of the sixth detector card.
            </v-card-text>
            </v-card>
        </v-col>
    </v-row> -->

    <v-row>
      <div v-if="isLoading" class="loading-indicator">
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </div>
      <v-card class="main-response-card" v-else>
        <v-card-title>Detector Result</v-card-title>
        <v-card-text>
          <div v-if="apiResponse">
            <p>
              <strong>Final Label:</strong> {{ apiResponse.final_label }}
            </p>
            <p><strong>Score:</strong> {{ apiResponse.score }}</p>
            <v-expansion-panels class="mt-4">
              <v-expansion-panel>
                <v-expansion-panel-title> Details </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <div
                    v-for="(detail, key) in apiResponse.details"
                    :key="key"
                    class="mb-4"
                  >
                    <h3>{{ key }}</h3>
                    <p><strong>Label:</strong> {{ detail.label }}</p>
                    <p><strong>Confidence:</strong> {{ detail.confidence }}</p>
                    <p v-if="detail.explanation">
                      <strong>Explanation:</strong> {{ detail.explanation }}
                    </p>
                    <p v-if="detail.overlap_score">
                      <strong>Overlap Score:</strong> {{ detail.overlap_score }}
                    </p>
                    <p v-if="detail.search_terms && detail.search_terms.length">
                      <strong>Search Terms:</strong>
                      {{ detail.search_terms.join(", ") }}
                    </p>
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

const apiResponse = ref("");
const userInput = ref("");
const isLoading = ref(false);

const getResult = () => {
  isLoading.value = true;
  axios
    .post("http://localhost:8000/predict", {
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

const responseExample = ref({
  final_label: "real",
  score: 0.539,
  details: {
    fn_result: {
      label: "fake",
      confidence: 0.6266951424523544,
      probabilities: { fake: 0.6266951424523544, real: 0.37330485754764564 },
    },
    wiki_result: {
      label: "real",
      confidence: 0,
      overlap_score: 1,
      search_terms: [
        "President",
        "Trump",
        "Donald Trump",
        "The United States",
        "The 45Th President",
      ],
    },
    scraper_result: {
      label: "real",
      confidence: 0.9,
      explanation:
        "The claim is consistent with the extracted web triplets, which show Donald Trump as the president of United States. The specific claim about being the 45th president is also supported by multiple sources.",
    },
    coherence_result: {
      label: "real",
      confidence: 1,
      explanation:
        "The paragraph provides a factual statement about Donald Trump's presidency, which is coherent and makes sense.",
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
</style>
