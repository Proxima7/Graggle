<template>
    <div class="w-full">
      <input
        type="range"
        class="block w-full"
        :min="min"
        :max="max"
        :step="step"
        v-model="value"
        @input="handleValueChange"
      >
      <div class="mt-1 text-center">{{ value }}</div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        value: 0,
        min: 0,
        max: 5,
        step: 1,
      };
    },
    methods: {
      handleValueChange() {
        this.$emit('slider-value-updated', this.value);
      },
    }
  };
  </script>
  