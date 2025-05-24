<template>
  <div class="app">
    <h1>Knowledge Graph Explorer</h1>
    <input
        v-model="searchTerm"
        @input="onSearch"
        type="text"
        placeholder="Search for a concept..."
    />
    <GraphView v-if="triples.length" :triples="triples"/>
    <p v-else-if="searchTerm">No results for "{{ searchTerm }}"</p>
    <p v-else>Type a term to explore the graph.</p>
  </div>
</template>

<script setup>
import {ref} from 'vue';
import GraphView from './components/GraphView.vue';
import debounce from 'lodash/debounce';

const searchTerm = ref('');
const triples = ref([]);

const fetchTriples = async () => {
  if (!searchTerm.value.trim()) {
    triples.value = [];
    return;
  }

  const query = encodeURIComponent(searchTerm.value.trim());
  try {
    const res = await fetch(`http://localhost:8000/triples?q=${query}`);
    triples.value = await res.json();
  } catch (err) {
    console.error('Failed to fetch triples:', err);
    triples.value = [];
  }
};

const onSearch = debounce(fetchTriples, 2000);
</script>

<style scoped>
.app {
  max-width: 900px;
  margin: 2rem auto;
  font-family: sans-serif;
  text-align: center;
}

input {
  padding: 0.5rem 1rem;
  width: 60%;
  font-size: 1rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}
</style>
