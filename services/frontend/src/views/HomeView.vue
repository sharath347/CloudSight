<script setup lang="ts">
import { ref } from 'vue'
// import { ShieldCheck } from 'lucide-vue-next'

const selectedTab = ref('overview')

const accessKey = ref('')
const secretKey = ref('')
const region = ref('')
const errorMsg = ref('')

const handleSubmit = async () => {
  // Simple validation
  if (!accessKey.value || !secretKey.value || !region.value) {
    errorMsg.value = 'Please fill in all fields.'
    return
  }

  errorMsg.value = ''

  try {
    const response = await fetch('http://localhost:5000/run-scoutsuite', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        aws_access_key: accessKey.value,
        aws_secret_key: secretKey.value,
        region: region.value,
      }),
    })

    const result = await response.json()
    console.log('Success:', result)
  } catch (error) {
    console.error('Error:', error)
    errorMsg.value = 'Something went wrong. Please try again.'
  }
}
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
        <div v-if="selectedTab === 'aws'">
          <div class="m-4 flex justify-center align-middle">
            <img src="../assets/aws-svgrepo-com.svg" class="bg-white" alt="aws icon" width="64" height="64">
          </div>
          <h2 class="text-2xl font-semibold">Amazon Web Services</h2>
          <p class="mt-2 opacity-70">Connect your Amazon Web Services account to <br> enable security monitoring</p>
          <form @submit.prevent="handleSubmit">
            <fieldset class="flex flex-col fieldset rounded-box mt-4 p-4 justify-center align-middle space-y-4 items-center">
              <input type="text p-2 m-2 align-middle" placeholder="Access Key ID" class="input" v-model="accessKey"/>
              <input type="text p-2 m-2" placeholder="Secret Access Key" class="input" v-model="secretKey" />
              <input type="text p-2 m-2" placeholder="Region" class="input" v-model="region"/>
              <button class="btn btn-primary self-end mr-4">Connect Provider</button>
            </fieldset>
            <p v-if="errorMsg" class="text-red-500 text-sm mt-2">{{ errorMsg }}</p>
          </form>
          <!-- <fieldset class="fieldset rounded-box p-4 mt-4">

            <label class="label">Email</label>
            <input type="email" class="input" placeholder="Email" />

            <label class="label">Password</label>
            <input type="password" class="input" placeholder="Password" />

            <button class="btn btn-neutral mt-4">Login</button>
          </fieldset> -->
        </div>
      </div>
    </div>
  </div>

</template>
