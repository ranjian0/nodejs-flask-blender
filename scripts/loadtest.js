const axios = require('axios');
const { performance } = require('perf_hooks');

// Configuration
const serverURL = 'http://127.0.0.1:5000/data';
const numOfRequests = 10000; // Number of requests to send
const concurrentRequests = 50; // Number of concurrent requests to send
const requestBody = { command: 'cube' }; // POST request body

// Variables for statistics
let totalTime = 0;
let successfulRequests = 0;
let failedRequests = 0;

// Function to send a GET request
async function sendGetRequest() {
  const startTime = performance.now();
  try {
    await axios.get(serverURL);
    successfulRequests++;
  } catch (error) {
    failedRequests++;
    console.error(`GET request failed: ${error.message}`);
  }
  const endTime = performance.now();
  const duration = endTime - startTime;
  totalTime += duration;
}

// Function to send a POST request
async function sendPostRequest() {
  const startTime = performance.now();
  try {
    const resp = await axios.post(serverURL, requestBody);
    successfulRequests++;
    // console.error(`POST request success: ${resp.status}`);
  } catch (error) {
    failedRequests++;
    console.error(`POST request failed: ${error.message}`);
  }
  const endTime = performance.now();
  const duration = endTime - startTime;
  totalTime += duration;
}

// Function to calculate statistics and print the results
function printStatistics() {
  const averageLatency = totalTime / (successfulRequests + failedRequests);
  const throughput = (successfulRequests / totalTime) * 1000; // Requests per second

  console.log('---------------------');
  console.log('Load Test Statistics:');
  console.log('---------------------');
  console.log(`Total Requests: ${numOfRequests}`);
  console.log(`Successful Requests: ${successfulRequests}`);
  console.log(`Failed Requests: ${failedRequests}`);
  console.log(`Total Time: ${totalTime.toFixed(2)} milliseconds`);
  console.log(`Average Latency: ${averageLatency.toFixed(2)} milliseconds`);
  console.log(`Throughput: ${throughput.toFixed(2)} requests per second`);
  console.log('---------------------');
}

// Function to run load test
async function runLoadTest() {
  console.log(`Starting load test with ${numOfRequests} requests...`);
  console.log('----------------------------------------');

  const promises = [];

  for (let i = 0; i < numOfRequests; i++) {
    if (i % concurrentRequests === 0) {
      await Promise.all(promises);
      promises.length = 0;
    }

    promises.push(sendPostRequest());
  }

  await Promise.all(promises);
  console.log('----------------------------------------');
  console.log('Load test completed.');
  printStatistics();
}

runLoadTest().catch(console.error);
