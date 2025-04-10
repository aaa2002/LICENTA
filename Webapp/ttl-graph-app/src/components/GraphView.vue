<template>
  <div ref="cyContainer" style="width: 900px; height: 600px; display: flex;" class="cy-container"></div>
</template>

<script setup>
import {ref, onMounted, watch} from 'vue';
import cytoscape from 'cytoscape';
import {clean} from '../helpers/methods.js'; // ✅ using your existing helper

const props = defineProps({
  triples: Array
});

const cyContainer = ref(null);
let cy = null;

const renderGraph = () => {
  if (!cyContainer.value) return;

  const nodeMap = new Map();
  const edges = [];

  props.triples.forEach(triple => {
    const subj = clean(triple.subject.value);
    const obj = clean(triple.object.value);
    const pred = clean(triple.predicate.value);

    if (!nodeMap.has(subj)) nodeMap.set(subj, {data: {id: subj, label: subj}});
    if (!nodeMap.has(obj)) nodeMap.set(obj, {data: {id: obj, label: obj}});

    edges.push({
      data: {
        id: `${subj}_${obj}_${pred}`,
        source: subj,
        target: obj,
        label: pred
      }
    });
  });

  const elements = [...nodeMap.values(), ...edges];

  if (cy) cy.destroy();

  cy = cytoscape({
    container: cyContainer.value,
    elements,
    style: [
      {
        selector: 'node',
        style: {
          label: 'data(label)',
          'background-color': '#007bff',
          'color': '#fff',
          'text-valign': 'center',
          'text-halign': 'center',
          'font-size': '12px'
        }
      },
      {
        selector: 'edge',
        style: {
          label: 'data(label)',
          'curve-style': 'bezier',
          'target-arrow-shape': 'triangle',
          'line-color': '#ccc',
          'target-arrow-color': '#ccc',
          'font-size': '10px',
          'text-margin-y': -10
        }
      }
    ],
    layout: {name: 'cose'}
  });
};

watch(() => props.triples, renderGraph, {immediate: true});
onMounted(renderGraph);
</script>

<style>
.cy-container {
  border: 1px solid #ccc;
  border-radius: 6px;

  div:first-child {
      display: flex;
  }
}
</style>
