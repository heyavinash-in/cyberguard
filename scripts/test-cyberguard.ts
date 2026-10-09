import { runUrlAnalysisPipeline } from '../src/lib/url-analyzer/pipeline';
import { runMessageAnalysisPipeline } from '../src/lib/message-analyzer/pipeline';

const testUrls = [
  "https://github.com/login", // Legitimate HTTPS website containing login
  "http://192.168.1.1/admin", // IP-based URL
  "https://accounts-gitam.edu.login-security.net/verify", // Brand impersonation + Suspicious subdomain
  "https://paypa1-example.net/login", // Suspicious login page / Typosquat
  "http://example.com:8080/secure", // Unusual port + HTTP
  "https://very-long-url-example.com/" + "a".repeat(150), // Long URL
  "https://a.b.c.d.e.f.example.com", // Excessive subdomains
  "https://bit.ly/3xYz4", // URL shortener
  "https://google.com@example.net", // Encoded/Obfuscated
  "https://netflix.com" // Legitimate URL
];

const testMessages = [
  "Hey, are we still meeting for lunch today?", // Normal message
  "URGENT: Your account has been temporarily suspended. Verify your identity immediately or you will lose access.", // Urgent credential request
  "A/c XX5184 Credited with Rs.5000. Report Dispute https://spgrs.ucoonline.bank.in", // Real bank message
  "This is the university administration office. Your student portal access will be revoked unless you send me your password.", // Fake university authority
  "You have won a reward of $50,000! Click here to claim.", // Suspicious payment request
  "Don't forget your assignment is due tomorrow." // Normal promotional/educational
];

async function runTests() {
  console.log("=========================================");
  console.log("   CYBERGUARD END-TO-END TEST SUITE      ");
  console.log("=========================================\\n");

  let urlCorrect = 0;
  for (const url of testUrls) {
    try {
      const res = await runUrlAnalysisPipeline(url);
      console.log(`[URL Test] ${url.substring(0, 50)}...`);
      console.log(`  Verdict: ${res.classification.label} | Risk: ${res.classification.risk_score} | Confidence: ${res.classification.confidence * 100}%`);
      console.log(`  Summary: ${res.summary}`);
      console.log(`  Severity: ${res.classification.severity}`);
      console.log("-----------------------------------------");
    } catch(e) {
      console.log(`[URL Test Failed] ${url}`, e);
    }
  }

  console.log("\\n=========================================\\n");

  for (const msg of testMessages) {
    try {
      const res = await runMessageAnalysisPipeline(msg);
      console.log(`[Message Test] "${msg.substring(0, 50)}..."`);
      console.log(`  Verdict: ${res.verdict} | Risk: ${res.riskScore} | Confidence: ${res.confidence}%`);
      console.log(`  Summary: ${res.explanation}`);
      console.log("-----------------------------------------");
    } catch(e) {
      console.log(`[Message Test Failed]`, e);
    }
  }

  console.log("\\nTest Run Complete.");
}

runTests();
