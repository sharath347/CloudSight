<script setup lang="ts">
import { ref } from 'vue'
import { ShieldCheck } from 'lucide-vue-next'

const selectedTab = ref('overview')
</script>

<template>
  <div class="inline-flex tabs tabs-box w-[1/4] m-6">
    <input
      type="radio"
      name="my_tabs_6"
      class="tab"
      aria-label="Overview"
      value="overview"
      v-model="selectedTab"
      checked="checked"
    />

    <input
      type="radio"
      name="my_tabs_6"
      class="tab"
      aria-label="AWS"
      value="aws"
      v-model="selectedTab"
    />

    <input
      type="radio"
      name="my_tabs_6"
      class="tab"
      aria-label="Azure"
      value="azure"
      v-model="selectedTab"
    />

    <input
      type="radio"
      name="my_tabs_6"
      class="tab"
      aria-label="Google Cloud"
      value="googlecloud"
      v-model="selectedTab"
    />
  </div>

  <!-- <div class="m-6">
    <div class="h-screen w-full bg-base-100 rounded-2xl shadow flex items-center justify-center">
      <div class="text-center">
        <h1 class="text-2xl font-bold mb-2 capitalize">{{ selectedTab }}</h1>
        <p class="text-gray-600">You selected the <strong>{{ selectedTab }}</strong> tab.</p>
      </div>
    </div>
  </div> -->
  <!-- Card Area -->
  <div class="flex-1 mt-0 m-6">
    <div class="w-full grow bg-base-100 rounded-2xl shadow flex flex-col items-center justify-center overflow-hidden">
      <div class="text-center">
        <div v-if="selectedTab === 'overview'">
          <h2 class="text-3xl font-bold">Welcome to Cloud Security Dashboard</h2>
          <p class="mt-2">Get started by connecting your cloud providers. We'll </p>
          <p>help you monitor and secure your cloud infrastructure</p>
          <p> across AWS, Azure, and Google Cloud.</p>


        </div>
      </div>
    </div>
  </div>

</template>
