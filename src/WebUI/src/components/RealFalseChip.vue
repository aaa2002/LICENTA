<template>
  <div>
    <span
      class="chip"
      :class="label === 'real' ? 'chip-success' : 'chip-error'"
    >
      {{ label }}
    </span>
  </div>
</template>

<script setup>
const props = defineProps({
  label: {
    type: String,
    required: true,
  },
});
</script>

<style>
.chip {
  display: inline-block;
  padding: 0 16px;
  width: 92px;
  border-radius: 8px;
  font-size: 0.875rem;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-transform: capitalize;
  font-weight: bold;
  color: rgb(var(--v-theme-on-surface-variant));
  background-color: rgb(var(--v-theme-primary-container));
}

.chip-success {
  background-color: rgb(var(--v-theme-success-lighten-3)) !important;
  color: rgb(var(--v-theme-success)) !important;
}

.chip-error {
  background-color: rgb(var(--v-theme-error-lighten-3)) !important;
  color: rgb(var(--v-theme-error)) !important;
}
</style>
