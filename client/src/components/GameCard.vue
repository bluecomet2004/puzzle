<script setup lang="ts">
const props = defineProps(['data']);
const emit = defineEmits(['change']);

function toggleOpen() {
  emit('change', {
    ...props.data,
    open: !props.data.open,
    hint: false,
    matched: false
  });
}
</script>

<template>
  <div
    @click="toggleOpen"
    :class="props.data.hint ? 'hint' : props.data.matched ? 'matched' : props.data.open ? 'active' : ''"
  >
    <span></span>
    <slot></slot>
  </div>
</template>