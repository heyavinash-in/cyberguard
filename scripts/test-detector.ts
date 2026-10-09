import * as fs from 'fs';
import * as path from 'path';
import { detectPhishing } from '../src/lib/phishing-detector';

function runTests() {
  const dataPath = path.join(__dirname, '../data/phishing_dataset.json');
  const dataset = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));

  let total = 0;
  let correct = 0;
  
  // For binary metrics: treat "SAFE" as Negative, everything else as Positive (Malicious)
  let truePositives = 0;
  let falsePositives = 0;
  let trueNegatives = 0;
  let falseNegatives = 0;

  console.log("=========================================");
  console.log(" CyberGuard Phishing Detector Test Run ");
  console.log("=========================================n");

  for (const item of dataset) {
    total++;
    const result = detectPhishing(item.message);
    
    // Check if the multi-class label matches exactly
    const isExactMatch = result.label === item.label;
    if (isExactMatch) correct++;

    // Binary Evaluation (Is it correctly identifying threats vs safe?)
    const actualIsThreat = item.label !== "SAFE";
    const predictedIsThreat = result.label !== "SAFE";

    if (actualIsThreat && predictedIsThreat) truePositives++;
    else if (!actualIsThreat && predictedIsThreat) falsePositives++;
    else if (!actualIsThreat && !predictedIsThreat) trueNegatives++;
    else if (actualIsThreat && !predictedIsThreat) falseNegatives++;

    if (!isExactMatch) {
      console.log(`[MISMATCH] Example ${item.id}`);
      console.log(`  Actual: ${item.label}, Predicted: ${result.label}`);
      console.log(`  Message: "${item.message.substring(0, 50)}..."`);
    }
  }

  const accuracy = (correct / total) * 100;
  const binaryAccuracy = ((truePositives + trueNegatives) / total) * 100;
  const precision = truePositives / (truePositives + falsePositives) || 0;
  const recall = truePositives / (truePositives + falseNegatives) || 0;
  const f1 = 2 * (precision * recall) / (precision + recall) || 0;

  console.log("n=========================================");
  console.log("           EVALUATION METRICS          ");
  console.log("=========================================");
  console.log(`Total Examples Tested: ${total}`);
  console.log(`Exact Label Match Accuracy: ${accuracy.toFixed(2)}%`);
  console.log(`Threat Detection (Binary) Accuracy: ${binaryAccuracy.toFixed(2)}%`);
  console.log(`nTrue Positives (Threats Caught): ${truePositives}`);
  console.log(`True Negatives (Safe Allowed): ${trueNegatives}`);
  console.log(`False Positives (Safe Flagged): ${falsePositives}`);
  console.log(`False Negatives (Threats Missed): ${falseNegatives}`);
  console.log(`nPrecision: ${(precision * 100).toFixed(2)}%`);
  console.log(`Recall: ${(recall * 100).toFixed(2)}%`);
  console.log(`F1 Score: ${(f1 * 100).toFixed(2)}%`);
  console.log("=========================================");
}

runTests();
