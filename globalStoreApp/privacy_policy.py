from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse


def privacy_policy(request):
    html_content = '''
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Privacy Policy - QuickCommerse</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.7;
      margin: 20px;
      background-color: #f9f9f9;
      color: #333;
    }
    h1, h2 {
      color: #2c3e50;
    }
    h1 {
      border-bottom: 2px solid #ccc;
      padding-bottom: 10px;
    }
    section {
      margin-bottom: 30px;
    }
  </style>
</head>
<body>

  <h1>Privacy Policy for QuickCommerse</h1>
  <p><strong>Effective Date:</strong> [Insert Date]</p>

  <section>
    <h2>1. Information We Collect</h2>
    <p>We collect the following types of information when you use QuickCommerse as a <strong>buyer</strong>, <strong>seller</strong>, or <strong>delivery partner</strong>:</p>
    <ul>
      <li><strong>Personal Information:</strong> Full name, email address, mobile number, address, government ID (for delivery partners), bank/UPI details.</li>
      <li><strong>Device & Usage Information:</strong> Device ID, OS, browser type, IP address, location, app usage data.</li>
      <li><strong>Transactional Information:</strong> Purchase/sale history, delivery records, order preferences.</li>
    </ul>
  </section>

  <section>
    <h2>2. How We Use Your Information</h2>
    <p>We use the collected data to:</p>
    <ul>
      <li>Create and manage your account</li>
      <li>Match buyers, sellers, and delivery partners</li>
      <li>Process payments and payouts</li>
      <li>Deliver orders efficiently</li>
      <li>Provide customer support</li>
      <li>Improve app performance</li>
      <li>Send alerts, offers, and updates</li>
      <li>Comply with legal obligations</li>
    </ul>
  </section>

  <section>
    <h2>3. Sharing Your Information</h2>
    <p>We do <strong>not sell</strong> your personal data. However, we may share your information with:</p>
    <ul>
      <li>Other users (e.g., delivery addresses, delivery instructions)</li>
      <li>Third-party service providers (e.g., payments, SMS/email)</li>
      <li>Legal authorities (when required by law)</li>
      <li>Business affiliates (in case of mergers/acquisitions)</li>
    </ul>
  </section>

  <section>
    <h2>4. Data Security</h2>
    <p>We use technical and organizational measures to protect your data. However, no method of transmission or storage is 100% secure.</p>
  </section>

  <section>
    <h2>5. Your Rights and Choices</h2>
    <p>Depending on your region, you may have the right to:</p>
    <ul>
      <li>Access or correct your data</li>
      <li>Request data deletion</li>
      <li>Opt-out of marketing</li>
      <li>Withdraw consent</li>
    </ul>
    <p>You can manage most settings from within the app or by contacting us.</p>
  </section>

  <section>
    <h2>6. Children’s Privacy</h2>
    <p>QuickCommerse is not intended for individuals under the age of 18. We do not knowingly collect data from minors.</p>
  </section>

  <section>
    <h2>7. Changes to This Privacy Policy</h2>
    <p>We may update this policy from time to time. Significant changes will be notified via email or in-app notices.</p>
  </section>

  <section>
    <h2>8. Contact Us</h2>
    <p>If you have any questions or concerns about this Privacy Policy, please contact us at:</p>
    <p>
      <strong>QuickCommerse Privacy Team</strong><br>
      Email: <a href="mailto:your-email@example.com">your-email@example.com</a><br>
      Phone: [Your Phone Number]<br>
      Address: [Your Company Address]
    </p>
  </section>

</body>
</html>
    '''
    return HttpResponse(html_content)