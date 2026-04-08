<template>
  <div class="page">
    <div class="card">
      <h1>Crop Disease Diagnosis</h1>
      <p class="sub">Upload a crop image and get a diagnosis result.</p>

      <div class="form-row">
        <label>Crop Type</label>
        <select v-model="cropType">
          <option value="">Please Select</option>
          <option value="rice">Rice</option>
          <option value="tomato">Tomato</option>
          <option value="corn">Corn</option>
        </select>
      </div>

      <div class="form-row">
        <label>Image File</label>
        <input type="file" accept="image/*" @change="handleFileChange" />
      </div>

      <button :disabled="loading || !file" @click="handleUpload">
        {{ loading ? "Diagnosing..." : "Start Diagnosis" }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>

      <div v-if="result" class="result">
        <h2>Diagnosis Result</h2>
        <p><strong>Disease:</strong> {{ result.disease_name }}</p>
        <p><strong>Confidence:</strong> {{ result.confidence }}</p>
        <p><strong>Risk Level:</strong> {{ result.risk_level }}</p>
        <p><strong>Summary:</strong> {{ result.symptom_summary }}</p>

        <h3>Top-3 Predictions</h3>
        <ul>
          <li v-for="item in result.top3" :key="item.class_name">
            {{ item.class_name }} - {{ item.score }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { predictDisease } from "../api/diagnosis";

const cropType = ref("");
const file = ref(null);
const result = ref(null);
const loading = ref(false);
const error = ref("");

function handleFileChange(event) {
  const selected = event.target.files?.[0];
  file.value = selected || null;
}

async function handleUpload() {
  if (!file.value) {
    error.value = "Please choose an image first.";
    return;
  }

  loading.value = true;
  error.value = "";
  result.value = null;

  try {
    const res = await predictDisease(file.value, cropType.value);
    result.value = res.data;
  } catch (err) {
    error.value = err?.response?.data?.detail || "Upload failed.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f4f8f2;
  padding: 40px 20px;
}

.card {
  max-width: 760px;
  margin: 0 auto;
  background: #ffffff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

h1 {
  margin: 0 0 8px;
}

.sub {
  color: #666;
  margin-bottom: 24px;
}

.form-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

label {
  margin-bottom: 8px;
  font-weight: 600;
}

input,
select {
  padding: 10px 12px;
  border: 1px solid #cfd8cc;
  border-radius: 8px;
}

button {
  background: #2f8f4e;
  color: #fff;
  border: none;
  padding: 12px 20px;
  border-radius: 10px;
  cursor: pointer;
  margin-top: 8px;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.result {
  margin-top: 28px;
  padding: 20px;
  background: #f8fbf7;
  border-radius: 12px;
}

.error {
  color: #d33;
  margin-top: 16px;
}
</style>
