<script setup lang="ts">
</script>

<template>
  <main>
    <div class="mx-auto p-4 md:p-8">
      <!-- name of each tab group should be unique -->
      <div class="tabs tabs-box">
        <input type="radio" name="my_tabs_6" class="tab" aria-label="Overview" />
        <div class="tab-content bg-base-100 border-base-300 p-6">Tab content 1</div>

        <input type="radio" name="my_tabs_6" class="tab" aria-label="AWS" checked="checked" />
        <div class="tab-content bg-base-100 border-base-300 p-6">Tab content 2</div>

        <input type="radio" name="my_tabs_6" class="tab" aria-label="Azure" />
        <div class="tab-content bg-base-100 border-base-300 p-6">Tab content 3</div>

        <input type="radio" name="my_tabs_6" class="tab" aria-label="Google Cloud" />
        <div class="tab-content bg-base-100 border-base-300 p-6">Tab content 4</div>
      </div>
    </div>
  </main>
</template>
