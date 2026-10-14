document.addEventListener('DOMContentLoaded', () => {

      /* ─────────────────────────────────────────────────
         SESSION CHECK
         ───────────────────────────────────────────────── */
      function getSession() {
        const session = sessionStorage.getItem('virevo-session');
        return session ? JSON.parse(session) : null;
      }

      const session = getSession();
      if (!session || !session.loggedIn) {
        // Not logged in, redirect to index
        window.location.href = 'index.html';
        return;
      }


      /* ─────────────────────────────────────────────────
         PARTICLES
         ───────────────────────────────────────────────── */
      const particlesEl = document.getElementById('particles');
      if (particlesEl) {
        for (let i = 0; i < 25; i++) {
          const p = document.createElement('div');
          p.className = 'particle';
          p.style.left = Math.random() * 100 + '%';
          p.style.top = Math.random() * 100 + '%';
          p.style.animationDelay = Math.random() * 6 + 's';
          p.style.animationDuration = (4 + Math.random() * 4) + 's';
          if (Math.random() > 0.5) p.style.background = 'var(--gold)';
          particlesEl.appendChild(p);
        }
      }


      /* ─────────────────────────────────────────────────
         THEME SWITCHER
         ───────────────────────────────────────────────── */
      const themeBtn = document.getElementById('themeBtn');
      const themeDD = document.getElementById('themeDropdown');
      const themeWrapper = document.getElementById('themeWrapper');

      // Load saved theme
      const savedTheme = localStorage.getItem('virevo-theme');
      if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        document.querySelectorAll('.theme-option').forEach(o => {
          o.classList.toggle('active', o.dataset.theme === savedTheme);
        });
      }

      themeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        themeDD.classList.toggle('open');
      });

      document.addEventListener('click', (e) => {
        if (!themeWrapper.contains(e.target)) {
          themeDD.classList.remove('open');
        }
      });

      themeDD.addEventListener('click', (e) => {
        e.stopPropagation();
      });

      document.querySelectorAll('.theme-option').forEach(option => {
        option.addEventListener('click', () => {
          const theme = option.dataset.theme;
          document.documentElement.setAttribute('data-theme', theme);
          localStorage.setItem('virevo-theme', theme);
          document.querySelectorAll('.theme-option').forEach(o => o.classList.remove('active'));
          option.classList.add('active');
          setTimeout(() => themeDD.classList.remove('open'), 350);
        });
      });


      /* ─────────────────────────────────────────────────
         GET QUERY FROM SESSION
         ───────────────────────────────────────────────── */
      const userQuery = sessionStorage.getItem('virevo-query') || '';
      const attachments = JSON.parse(sessionStorage.getItem('virevo-attachments') || '[]');
      const userName = session.name.split(' ')[0];


      /* ─────────────────────────────────────────────────
         CHAT MESSAGES AREA
         ───────────────────────────────────────────────── */
      const chatMessagesArea = document.getElementById('chatMessagesArea');
      const analysisContent = document.getElementById('analysisContent');

      function addChatMessage(type, content, time) {
        const msg = document.createElement('div');
        msg.className = `chat-msg ${type}`;
        msg.innerHTML = `
          <div class="msg-bubble">${content}</div>
          <div class="msg-time">${time || new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
        `;
        chatMessagesArea.appendChild(msg);
        chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight;
        return msg;
      }

      function addProcessingStatus() {
        const status = document.createElement('div');
        status.className = 'chat-msg assistant';
        status.id = 'processingStatus';
        status.innerHTML = `
          <div class="processing-status">
            <div class="status-header">
              <div class="spinner-mini"></div>
              <span>Analyzing your query...</span>
            </div>
            <div class="status-item" id="step1">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
              Parsing request
            </div>
            <div class="status-item" id="step2">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
              Gathering data
            </div>
            <div class="status-item" id="step3">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
              Running analysis
            </div>
            <div class="status-item" id="step4">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
              Generating results
            </div>
          </div>
        `;
        chatMessagesArea.appendChild(status);
        chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight;
        return status;
      }

      function updateProcessingStep(stepId, done) {
        const step = document.getElementById(stepId);
        if (step) {
          step.classList.toggle('done', done);
          step.innerHTML = done 
            ? `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> ${step.textContent.trim()}`
            : step.innerHTML;
        }
      }


      /* ─────────────────────────────────────────────────
         RENDER ANALYSIS RESULTS
         ───────────────────────────────────────────────── */
      function renderAnalysisResults(query) {
        // Helper function to generate tree structure with expandable details
        function generateTreeBranches(causeNum) {
          const nodeData = [
            {
              id: 'process-flow',
              title: 'Show the Process Flow',
              icon: '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
              iconStyle: '',
              content: `
                <div class="node-detail-section">
                  <div class="node-detail-label">Current Process Flow</div>
                  <div class="node-detail-text">Visual representation of the existing workflow from initiation to completion.</div>
                  <div class="process-flow">
                    <div class="flow-step">
                      <div class="flow-step-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l2 2"/></svg>
                      </div>
                      <span class="flow-step-label">Request Initiation</span>
                    </div>
                    <div class="flow-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
                    <div class="flow-step">
                      <div class="flow-step-icon" style="background: rgba(197, 160, 68, 0.15); color: var(--gold);">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/></svg>
                      </div>
                      <span class="flow-step-label">Data Collection</span>
                    </div>
                    <div class="flow-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
                    <div class="flow-step">
                      <div class="flow-step-icon" style="background: rgba(68, 130, 197, 0.15); color: #68a8d4;">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
                      </div>
                      <span class="flow-step-label">Processing</span>
                    </div>
                    <div class="flow-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
                    <div class="flow-step">
                      <div class="flow-step-icon" style="background: rgba(140, 68, 197, 0.15); color: #a878d4;">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
                      </div>
                      <span class="flow-step-label">Review</span>
                    </div>
                    <div class="flow-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
                    <div class="flow-step">
                      <div class="flow-step-icon" style="background: rgba(68, 197, 140, 0.15); color: #68d4a8;">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                      </div>
                      <span class="flow-step-label">Completion</span>
                    </div>
                  </div>
                </div>
                <div class="node-detail-section">
                  <div class="node-detail-label">Flow Summary</div>
                  <div class="node-detail-text">
                    The current process involves 5 sequential stages with an average cycle time of 12 days. Data shows 23% of requests experience delays at the Processing stage due to manual handoffs.
                  </div>
                </div>
              `
            },
            {
              id: 'bottlenecks',
              title: 'Bottlenecks in Process',
              icon: '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>',
              iconStyle: 'background: rgba(197, 160, 68, 0.15); color: var(--gold);',
              content: `
                <div class="node-detail-section">
                  <div class="node-detail-label">Identified Bottlenecks</div>
                  <div class="node-detail-text">Critical points where workflow efficiency is compromised:</div>
                  <div class="bottleneck-list">
                    <div class="bottleneck-item">
                      <div class="bottleneck-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                      </div>
                      <span class="bottleneck-text">Manual data entry causing 3-4 hour delays per request</span>
                      <span class="bottleneck-severity high">High</span>
                    </div>
                    <div class="bottleneck-item">
                      <div class="bottleneck-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
                      </div>
                      <span class="bottleneck-text">Single approver dependency creating queue backlog</span>
                      <span class="bottleneck-severity medium">Medium</span>
                    </div>
                    <div class="bottleneck-item">
                      <div class="bottleneck-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
                      </div>
                      <span class="bottleneck-text">Legacy system integration issues causing data sync failures</span>
                      <span class="bottleneck-severity low">Low</span>
                    </div>
                  </div>
                </div>
                <div class="node-detail-section">
                  <div class="node-detail-label">Impact Assessment</div>
                  <div class="node-detail-text">
                    These bottlenecks collectively account for 67% of all process delays. Addressing the high-severity issues alone could reduce cycle time by 40%.
                  </div>
                </div>
              `
            },
            {
              id: 'changes',
              title: 'Changes Recommended',
              icon: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
              iconStyle: 'background: rgba(68, 130, 197, 0.15); color: #68a8d4;',
              content: `
                <div class="node-detail-section">
                  <div class="node-detail-label">Recommended Changes</div>
                  <div class="node-detail-text">Strategic modifications to optimize the workflow:</div>
                  <div class="recommendation-cards">
                    <div class="recommendation-card">
                      <div class="recommendation-card-icon" style="background: var(--green-glow); color: var(--green-light);">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/></svg>
                      </div>
                      <h5>Automation Implementation</h5>
                      <p>Deploy RPA for data entry tasks to eliminate manual processing delays.</p>
                    </div>
                    <div class="recommendation-card">
                      <div class="recommendation-card-icon" style="background: rgba(197, 160, 68, 0.15); color: var(--gold);">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                      </div>
                      <h5>Parallel Approval Workflow</h5>
                      <p>Enable multiple approvers to work simultaneously and reduce bottlenecks.</p>
                    </div>
                    <div class="recommendation-card">
                      <div class="recommendation-card-icon" style="background: rgba(68, 130, 197, 0.15); color: #68a8d4;">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
                      </div>
                      <h5>API Integration</h5>
                      <p>Modernize system connections with RESTful APIs for real-time data sync.</p>
                    </div>
                  </div>
                </div>
              `
            },
            {
              id: 'cost',
              title: 'Cost Implications',
              icon: '<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
              iconStyle: 'background: rgba(140, 68, 197, 0.15); color: #a878d4;',
              content: `
                <div class="node-detail-section">
                  <div class="node-detail-label">Cost Breakdown</div>
                  <div class="node-detail-text">Estimated investment required for recommended changes:</div>
                  <table class="cost-table">
                    <thead>
                      <tr>
                        <th>Item</th>
                        <th>Category</th>
                        <th>Estimate</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>RPA Implementation</td>
                        <td>Software</td>
                        <td class="cost-value">$45,000</td>
                      </tr>
                      <tr>
                        <td>System Integration</td>
                        <td>Development</td>
                        <td class="cost-value">$32,000</td>
                      </tr>
                      <tr>
                        <td>Training & Change Mgmt</td>
                        <td>Operations</td>
                        <td class="cost-value">$18,000</td>
                      </tr>
                      <tr class="total-row">
                        <td colspan="2"><strong>Total Investment</strong></td>
                        <td class="cost-value">$95,000</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="node-detail-section">
                  <div class="node-detail-label">ROI Projection</div>
                  <div class="node-detail-text">
                    Expected annual savings of $180,000 through efficiency gains, resulting in ROI of 89% within the first year.
                  </div>
                </div>
              `
            },
            {
              id: 'simulation',
              title: 'Simulated Flow & Projections',
              icon: '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
              iconStyle: '',
              content: `
                <div class="node-detail-section">
                  <div class="node-detail-label">Performance Projections</div>
                  <div class="node-detail-text">Comparative analysis of current vs. optimized performance metrics:</div>
                  <div class="simulation-chart">
                    <div class="chart-bars">
                      <div class="chart-bar-group">
                        <div class="chart-bar current" style="height: 100%"></div>
                        <div class="chart-bar projected" style="height: 40%"></div>
                        <span class="chart-label">Cycle Time</span>
                      </div>
                      <div class="chart-bar-group">
                        <div class="chart-bar current" style="height: 80%"></div>
                        <div class="chart-bar projected" style="height: 25%"></div>
                        <span class="chart-label">Error Rate</span>
                      </div>
                      <div class="chart-bar-group">
                        <div class="chart-bar current" style="height: 60%"></div>
                        <div class="chart-bar projected" style="height: 90%"></div>
                        <span class="chart-label">Throughput</span>
                      </div>
                      <div class="chart-bar-group">
                        <div class="chart-bar current" style="height: 45%"></div>
                        <div class="chart-bar projected" style="height: 85%"></div>
                        <span class="chart-label">Customer Sat.</span>
                      </div>
                    </div>
                    <div class="chart-legend">
                      <div class="legend-item">
                        <div class="legend-color" style="background: var(--border);"></div>
                        <span>Current State</span>
                      </div>
                      <div class="legend-item">
                        <div class="legend-color" style="background: linear-gradient(to right, var(--green-primary), var(--green-light));"></div>
                        <span>Projected State</span>
                      </div>
                    </div>
                  </div>
                </div>
              `
            },
            {
              id: 'accept-costs',
              title: 'Ability to Change/Accept Costs',
              icon: '<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>',
              iconStyle: 'background: rgba(197, 160, 68, 0.15); color: var(--gold);',
              content: `
                <div class="node-detail-section">
                  <div class="node-detail-label">Flexibility Assessment</div>
                  <div class="node-detail-text">
                    Analysis of organizational readiness and cost acceptance capacity for proposed changes.
                  </div>
                  <div class="recommendation-cards">
                    <div class="recommendation-card">
                      <div class="recommendation-card-icon" style="background: rgba(68, 197, 140, 0.15); color: #68d4a8;">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                      </div>
                      <h5>Budget Availability</h5>
                      <p>Current fiscal quarter has approved budget allocation for process improvements.</p>
                    </div>
                    <div class="recommendation-card">
                      <div class="recommendation-card-icon" style="background: rgba(197, 160, 68, 0.15); color: var(--gold);">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                      </div>
                      <h5>Timeline Flexibility</h5>
                      <p>Implementation can be phased over 6 months to distribute costs and minimize disruption.</p>
                    </div>
                  </div>
                </div>
              `
            },
            {
              id: 'revised',
              title: 'Revised Simulation',
              icon: '<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>',
              iconStyle: 'background: rgba(68, 197, 140, 0.15); color: #68d4a8;',
              content: `
                <div class="node-detail-section">
                  <div class="node-detail-label">Revised Process Flow</div>
                  <div class="node-detail-text">Optimized workflow after implementing recommended changes:</div>
                  <div class="process-flow">
                    <div class="flow-step">
                      <div class="flow-step-icon" style="background: var(--green-glow); color: var(--green-light);">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83"/></svg>
                      </div>
                      <span class="flow-step-label">Auto-Intake</span>
                    </div>
                    <div class="flow-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
                    <div class="flow-step">
                      <div class="flow-step-icon" style="background: var(--green-glow); color: var(--green-light);">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/></svg>
                      </div>
                      <span class="flow-step-label">AI Processing</span>
                    </div>
                    <div class="flow-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
                    <div class="flow-step">
                      <div class="flow-step-icon" style="background: var(--green-glow); color: var(--green-light);">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                      </div>
                      <span class="flow-step-label">Auto-Approval</span>
                    </div>
                  </div>
                </div>
                <div class="node-detail-section">
                  <div class="node-detail-label">Improvement Metrics</div>
                  <div class="node-detail-text">
                    • Cycle time reduced from 12 days to 3 days (75% improvement)<br>
                    • Error rate decreased from 8% to 1.2%<br>
                    • Throughput increased by 150%
                  </div>
                </div>
              `
            },
            {
              id: 'description',
              title: 'Detailed Description',
              icon: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
              iconStyle: 'background: rgba(68, 130, 197, 0.15); color: #68a8d4;',
              content: `
                <div class="node-detail-section">
                  <div class="node-detail-label">Complete Analysis Summary</div>
                  <div class="node-detail-text">
                    This cause represents a significant factor contributing to the identified problem, accounting for approximately 30% of the overall impact. The root cause analysis reveals systemic inefficiencies that have developed over time due to organic growth without corresponding process optimization.
                  </div>
                </div>
                <div class="node-detail-section">
                  <div class="node-detail-label">Key Findings</div>
                  <div class="node-detail-text">
                    • Process inefficiency has compounded at 8% annually<br>
                    • Staff productivity affected by 23% due to manual workarounds<br>
                    • Customer satisfaction scores dropped 15 points over 2 years<br>
                    • Operational costs increased by $240,000 annually
                  </div>
                </div>
                <div class="node-detail-section">
                  <div class="node-detail-label">Strategic Recommendation</div>
                  <div class="node-detail-text">
                    A phased implementation approach is recommended, starting with high-impact, low-complexity changes in Q1, followed by major system integrations in Q2-Q3, with full optimization achieved by Q4.
                  </div>
                </div>
              `
            }
          ];

          return nodeData.map((node, index) => `
            <div class="tree-branch">
              <div class="tree-node" onclick="toggleNodeDetail('${causeNum}-${node.id}')" id="node-${causeNum}-${node.id}">
                <div class="tree-node-icon" style="${node.iconStyle}">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${node.icon}</svg>
                </div>
                <span class="tree-node-text">${node.title}</span>
                <svg class="tree-node-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="9 18 15 12 9 6"/>
                </svg>
              </div>
              <div class="node-detail-container" id="detail-${causeNum}-${node.id}">
                <div class="node-detail-content">
                  <div class="node-detail-header">
                    <div class="node-detail-header-icon" style="${node.iconStyle || 'background: var(--green-primary); color: #fff;'}">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${node.icon}</svg>
                    </div>
                    <h4>${node.title}</h4>
                  </div>
                  <div class="node-detail-body">
                    ${node.content}
                  </div>
                </div>
              </div>
            </div>
          `).join('');
        }

        analysisContent.innerHTML = `
          <!-- Query Analysis Container -->
          <div class="query-analysis-container">
            <div class="query-header">
              <div class="query-header-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"/>
                  <path d="M21 21l-4.35-4.35"/>
                </svg>
              </div>
              <div class="query-header-text">
                <h2>Query Analysis</h2>
                <p>Original Query: "${query}"</p>
              </div>
            </div>

            <div class="problems-container">
              <!-- Problems Sidebar -->
              <div class="problems-sidebar">
                <button class="problem-btn active" data-problem="1">P1 &middot; OT Utilisation</button>
                <button class="problem-btn" data-problem="2">P2 &middot; ICU Revenue</button>
                <button class="problem-btn" data-problem="3">P3 &middot; Margins</button>
                <button class="problem-btn" data-problem="4">P4 &middot; Cash Flow</button>
                <button class="problem-btn" data-problem="5">P5 &middot; Agency Nursing</button>
                <button class="problem-btn" data-problem="6">P6 &middot; Pharmacy Cost</button>
                <button class="problem-btn ai-gen" data-problem="7">AI-P1 &middot; Ward Round Timing</button>
                <button class="problem-btn ai-gen" data-problem="8">AI-P2 &middot; Biomedical Maintenance</button>
                <button class="problem-btn ai-gen" data-problem="9">AI-P3 &middot; Counsellor Incentives</button>
              </div>

              <!-- Problem Content Area -->
              <div class="problem-content-area">
                <!-- Tab Navigation -->
                <div class="problem-tabs">
                  <button class="tab-btn active" data-tab="analysis">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/></svg>
                    Analysis
                  </button>
                  <button class="tab-btn" data-tab="plan">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                    Plan
                  </button>
                  <button class="tab-btn" data-tab="cost">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>
                    Cost
                  </button>
                  <button class="tab-btn" data-tab="project">Project</button>
                </div>

                <!-- Tab Contents -->
                <div class="tab-content active" id="tab-analysis">
                  <!-- Problem Statement Dropdown -->
                  <div class="analysis-dropdown" id="dropdown-statement">
                    <div class="dropdown-header" onclick="toggleDropdown('dropdown-statement')">
                      <span class="dropdown-title" id="problem-statement-title">Problem Statement & Causes : P1 &middot; OT Utilisation</span>
                      <svg class="dropdown-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 12 15 18 9"/>
                      </svg>
                    </div>
                    <div class="dropdown-content" id="content-dropdown-statement">
                      <div class="analysis-item" style="animation-delay: 0.1s">
                        <div class="analysis-item-title">Problem Statement by Client</div>
                        <div class="analysis-item-content">
                          The client has identified operational inefficiencies in their current workflow process, leading to increased turnaround time and resource wastage.
                        </div>
                        
                        <!-- Problem Metrics Dashboard -->
                        <div class="problem-metrics-dashboard" id="problem-metrics-dashboard">
                           <div class="dashboard-header">
                              <div class="dashboard-titles">
                                 <h3 class="dashboard-main-title" id="dashboard-main-title">P1 — OT Utilisation Fluctuation</h3>
                                 <p class="dashboard-subtitle" id="dashboard-subtitle">OT Utilisation &middot; Baseline: 58% &rarr; Target: 76%</p>
                              </div>
                              <div class="dashboard-impact">
                                 <div class="impact-value" id="dashboard-impact-value">+₹68L/yr</div>
                                 <div class="impact-label">EBITDA Impact</div>
                              </div>
                           </div>
                           <div class="dashboard-cards">
                              <div class="metric-card">
                                 <div class="metric-value blue-text counter-animate" id="dashboard-baseline" data-target="58" data-suffix="%">0%</div>
                                 <div class="metric-label">BASELINE</div>
                              </div>
                              <div class="metric-card">
                                 <div class="metric-value green-text counter-animate" id="dashboard-target" data-target="76" data-suffix="%">0%</div>
                                 <div class="metric-label">TARGET</div>
                              </div>
                              <div class="metric-card">
                                 <div class="metric-value blue-text counter-animate" id="dashboard-actual" data-target="71.4" data-suffix="%" data-decimals="1">0%</div>
                                 <div class="metric-label" id="dashboard-actual-label">MONTH 6 ACTUAL</div>
                              </div>
                           </div>
                        </div>
                      </div>
                      <div class="diagnosis-comparison" style="animation-delay: 0.2s">
                        <div class="diagnosis-card owner-diagnosis">
                          <div class="diagnosis-header">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                              <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                            OWNER'S DIAGNOSIS
                          </div>
                          <div class="diagnosis-content">
                            <ul>
                              <li>Scheduling issues and frequent delays.</li>
                              <li>Unavailability of anaesthesia staff when required.</li>
                              <li>Unplanned doctor leaves affecting the timetable.</li>
                              <li>Patient drop-outs and slow admission process.</li>
                              <li>OT turnaround times are consistently high.</li>
                            </ul>
                          </div>
                        </div>
                        
                        <div class="diagnosis-card ai-diagnosis">
                          <div class="diagnosis-header">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                              <circle cx="12" cy="12" r="10"></circle>
                              <line x1="12" y1="16" x2="12" y2="12"></line>
                              <line x1="12" y1="8" x2="12.01" y2="8"></line>
                            </svg>
                            AI FINDING
                          </div>
                          <div class="diagnosis-content">
                            <ul>
                              <li>6 contributing causes identified — only 1 was scheduling-related.</li>
                              <li>Equipment maintenance backlog is a primary hidden driver.</li>
                              <li>Linen delays directly correlate with OT start time delays.</li>
                              <li>Post-op bed availability blocks new OT admissions in 30% cases.</li>
                              <li>Surgeon late arrivals average 45 mins in morning sessions.</li>
                              <li>Inadequate sterilization turnaround limits instrument availability.</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Mitigation Plan Dropdown -->
                  <div class="analysis-dropdown" id="dropdown-mitigation">
                    <div class="dropdown-header" onclick="toggleDropdown('dropdown-mitigation')">
                      <span class="dropdown-title">Mitigation Plan / Action</span>
                      <svg class="dropdown-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 12 15 18 9"/>
                      </svg>
                    </div>
                    <div class="dropdown-content" id="content-dropdown-mitigation">
                      <div class="mitigation-container">
                        <table class="mitigation-grid">
                          <thead>
                            <tr>
                              <th>Approve</th>
                              <th>Action</th>
                              <th>Owner</th>
                              <th>Mode</th>
                              <th>T/L Cost</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>
                                <label class="toggle-switch">
                                  <input type="checkbox" class="mitigation-approval-checkbox" onchange="checkMitigationApprovals()">
                                  <span class="toggle-slider"></span>
                                </label>
                              </td>
                              <td><div class="action-text">Automate scheduling integration between OPD and OT.</div></td>
                              <td>
                                <div class="owner-info">
                                  <span class="owner-name">Dr. A. Sharma</span>
                                  <span class="owner-dept">Operations Head</span>
                                </div>
                              </td>
                              <td>
                                <label class="toggle-switch">
                                  <input type="checkbox" checked>
                                  <span class="toggle-slider"></span>
                                </label>
                              </td>
                              <td><span class="cost-text green-text">₹ 15L/yr</span></td>
                            </tr>
                            <tr>
                              <td>
                                <label class="toggle-switch">
                                  <input type="checkbox" class="mitigation-approval-checkbox" onchange="checkMitigationApprovals()">
                                  <span class="toggle-slider"></span>
                                </label>
                              </td>
                              <td><div class="action-text">Recalibrate biomedical maintenance schedules dynamically.</div></td>
                              <td>
                                <div class="owner-info">
                                  <span class="owner-name">Mr. R. Mehta</span>
                                  <span class="owner-dept">Biomedical Dept</span>
                                </div>
                              </td>
                              <td>
                                <label class="toggle-switch">
                                  <input type="checkbox" checked>
                                  <span class="toggle-slider"></span>
                                </label>
                              </td>
                              <td><span class="cost-text green-text">₹ 8L/yr</span></td>
                            </tr>
                            <tr>
                              <td>
                                <label class="toggle-switch">
                                  <input type="checkbox" class="mitigation-approval-checkbox" onchange="checkMitigationApprovals()">
                                  <span class="toggle-slider"></span>
                                </label>
                              </td>
                              <td><div class="action-text">Implement real-time surgeon ETA tracking in mornings.</div></td>
                              <td>
                                <div class="owner-info">
                                  <span class="owner-name">Ms. S. Gupta</span>
                                  <span class="owner-dept">IT Director</span>
                                </div>
                              </td>
                              <td>
                                <label class="toggle-switch">
                                  <input type="checkbox">
                                  <span class="toggle-slider"></span>
                                </label>
                              </td>
                              <td><span class="cost-text green-text">₹ 12L/yr</span></td>
                            </tr>
                          </tbody>
                        </table>
                        
                        <div class="mitigation-actions">
                          <button class="btn-approve-mitigation" id="btn-final-approve" disabled onclick="approveAndGoToCost()">
                            Approve &amp; Analyze Cost
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                              <path d="M5 12h14"></path>
                              <path d="M12 5l7 7-7 7"></path>
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Our Analysis Dropdown -->
                  <div class="analysis-dropdown" id="dropdown-our-analysis">
                    <div class="dropdown-header" onclick="toggleDropdown('dropdown-our-analysis')">
                      <span class="dropdown-title">Our Analysis</span>
                      <svg class="dropdown-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 12 15 18 9"/>
                      </svg>
                    </div>
                    <div class="dropdown-content" id="content-dropdown-our-analysis">
                      <div class="analysis-item">
                        <div class="analysis-item-title">Identified Causes & Degree of Adjustability</div>
                        <div class="causes-list">
                          <!-- Cause 1 -->
                          <div>
                            <div class="cause-item" onclick="toggleCause(1)">
                              <span class="cause-name">Cause 1</span>
                              <div class="cause-percentage">
                                <div class="percentage-bar">
                                  <div class="percentage-fill" style="width: 30%"></div>
                                </div>
                                <span class="percentage-text">30%</span>
                              </div>
                              <span class="adjustability-badge">Adjustable</span>
                              <svg class="cause-expand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="9 18 15 12 9 6"/>
                              </svg>
                            </div>
                            <div class="tree-container" id="tree-cause-1">
                              <div class="tree-structure">
                                ${generateTreeBranches(1)}
                              </div>
                            </div>
                          </div>

                          <!-- Cause 2 -->
                          <div>
                            <div class="cause-item" onclick="toggleCause(2)">
                              <span class="cause-name">Cause 2</span>
                              <div class="cause-percentage">
                                <div class="percentage-bar">
                                  <div class="percentage-fill" style="width: 40%"></div>
                                </div>
                                <span class="percentage-text">40%</span>
                              </div>
                              <span class="adjustability-badge">Adjustable</span>
                              <svg class="cause-expand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="9 18 15 12 9 6"/>
                              </svg>
                            </div>
                            <div class="tree-container" id="tree-cause-2">
                              <div class="tree-structure">
                                ${generateTreeBranches(2)}
                              </div>
                            </div>
                          </div>

                          <!-- Cause 3 -->
                          <div>
                            <div class="cause-item" onclick="toggleCause(3)">
                              <span class="cause-name">Cause 3</span>
                              <div class="cause-percentage">
                                <div class="percentage-bar">
                                  <div class="percentage-fill" style="width: 30%"></div>
                                </div>
                                <span class="percentage-text">30%</span>
                              </div>
                              <span class="adjustability-badge">Adjustable</span>
                              <svg class="cause-expand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="9 18 15 12 9 6"/>
                              </svg>
                            </div>
                            <div class="tree-container" id="tree-cause-3">
                              <div class="tree-structure">
                                ${generateTreeBranches(3)}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="tab-content" id="tab-plan">
                  <div class="plan-content-layout">
                    <!-- Implementation Plan Grid -->
                    <div class="plan-section-card">
                      <div class="plan-section-header">
                        <span class="plan-section-title">IMPLEMENTATION PLAN — KEY INTERVENTIONS</span>
                      </div>
                      <table class="plan-grid-table">
                        <thead>
                          <tr>
                            <th class="col-timeline">TIMELINE</th>
                            <th class="col-num">#</th>
                            <th class="col-action">ACTION</th>
                            <th class="col-owner">OWNER</th>
                            <th class="col-mode">MODE</th>
                            <th class="col-progress">PROGRESS</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td class="timeline-cell"><strong>Wk 1–2</strong></td>
                            <td><span class="step-number">1</span></td>
                            <td>Activate HIS OT scheduling module and configure 48hr/2hr equipment checklist</td>
                            <td class="owner-cell">IT + Biomedical</td>
                            <td><span class="mode-badge offline"><span class="mode-dot"></span>OFFLINE</span></td>
                            <td class="progress-cell"><div class="mini-progress-bar"><div class="mini-progress-fill" style="width: 85%"></div></div><span class="progress-text">85%</span></td>
                          </tr>
                          <tr>
                            <td class="timeline-cell"><strong>Wk 2–4</strong></td>
                            <td><span class="step-number">2</span></td>
                            <td>Empanel third anaesthetist (visiting/part-time); implement 24hr pre-op confirmation SOP</td>
                            <td class="owner-cell">Dr. Mehta</td>
                            <td><span class="mode-badge offline"><span class="mode-dot"></span>OFFLINE</span></td>
                            <td class="progress-cell"><div class="mini-progress-bar"><div class="mini-progress-fill" style="width: 60%"></div></div><span class="progress-text">60%</span></td>
                          </tr>
                          <tr>
                            <td class="timeline-cell"><strong>Wk 4–6</strong></td>
                            <td><span class="step-number">3</span></td>
                            <td>Renegotiate linen vendor SLA to 60-min; install ward-level linen buffer stock</td>
                            <td class="owner-cell">Admin Head</td>
                            <td><span class="mode-badge offline"><span class="mode-dot"></span>OFFLINE</span></td>
                            <td class="progress-cell"><div class="mini-progress-bar"><div class="mini-progress-fill" style="width: 40%"></div></div><span class="progress-text">40%</span></td>
                          </tr>
                          <tr>
                            <td class="timeline-cell"><strong>Wk 6–8</strong></td>
                            <td><span class="step-number">4</span></td>
                            <td>Launch preventive maintenance calendar for all OT-critical equipment (AI-P2)</td>
                            <td class="owner-cell">Biomedical Engineer</td>
                            <td><span class="mode-badge online"><span class="mode-dot"></span>ONLINE</span></td>
                            <td class="progress-cell"><div class="mini-progress-bar"><div class="mini-progress-fill" style="width: 20%"></div></div><span class="progress-text">20%</span></td>
                          </tr>
                          <tr>
                            <td class="timeline-cell"><strong>Wk 8–12</strong></td>
                            <td><span class="step-number">5</span></td>
                            <td>Monitor OT utilisation weekly; adaptive nudge to surgeons for unfilled slots via HIS</td>
                            <td class="owner-cell">Virevo / COO</td>
                            <td><span class="mode-badge online"><span class="mode-dot"></span>ONLINE</span></td>
                            <td class="progress-cell"><div class="mini-progress-bar"><div class="mini-progress-fill" style="width: 10%"></div></div><span class="progress-text">10%</span></td>
                          </tr>
                        </tbody>
                      </table>
                    </div>

                    <!-- Anticipated Implementation Hurdles -->
                    <div class="hurdles-section-card">
                      <div class="hurdles-section-header">
                        <span class="hurdles-icon">⚠</span>
                        <span class="hurdles-title">ANTICIPATED IMPLEMENTATION HURDLES</span>
                      </div>
                      <div class="hurdles-grid">
                        <div class="hurdle-card">
                          <span class="hurdle-icon">⚠</span>
                          <span class="hurdle-text">Anaesthetists resistant to advance booking — prefer flexibility</span>
                        </div>
                        <div class="hurdle-card">
                          <span class="hurdle-icon">⚠</span>
                          <span class="hurdle-text">Linen vendor will push back on SLA penalty clauses</span>
                        </div>
                        <div class="hurdle-card">
                          <span class="hurdle-icon">⚠</span>
                          <span class="hurdle-text">Surgeons reluctant to commit slots 48hrs in advance</span>
                        </div>
                        <div class="hurdle-card">
                          <span class="hurdle-icon">⚠</span>
                          <span class="hurdle-text">IT team capacity constraint for HIS module configuration</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="tab-content" id="tab-cost">
                  <div class="cost-analysis-layout">
                    <!-- Left: Implementation Cost Breakdown -->
                    <div class="cost-main-section">
                      <div class="cost-section-card">
                        <div class="cost-section-header">
                          <span class="cost-section-icon">💰</span>
                          <span class="cost-section-title">IMPLEMENTATION COST BREAKDOWN</span>
                        </div>
                        <table class="cost-breakdown-table">
                          <thead>
                            <tr>
                              <th class="col-item">ITEM</th>
                              <th class="col-type">TYPE</th>
                              <th class="col-cost">COST (₹)</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>HIS OT Scheduling Module Configuration</td>
                              <td><span class="type-badge one-time">One-time</span></td>
                              <td class="cost-value">₹80,000</td>
                            </tr>
                            <tr>
                              <td>Biomedical Engineer (part-time, ₹18k/month)</td>
                              <td><span class="type-badge recurring">Recurring</span></td>
                              <td class="cost-value">₹2.2L</td>
                            </tr>
                            <tr>
                              <td>Equipment PM — parts & labour (annual)</td>
                              <td><span class="type-badge recurring">Recurring</span></td>
                              <td class="cost-value">₹1.2L</td>
                            </tr>
                            <tr>
                              <td>Linen Buffer Stock (ward-level)</td>
                              <td><span class="type-badge one-time">One-time</span></td>
                              <td class="cost-value">₹45,000</td>
                            </tr>
                            <tr>
                              <td>Anaesthetist empanelment (visiting)</td>
                              <td><span class="type-badge recurring">Recurring</span></td>
                              <td class="cost-value">₹2.4L</td>
                            </tr>
                            <tr class="total-row">
                              <td><strong>One-time Total</strong></td>
                              <td></td>
                              <td class="cost-value"><strong>₹1.3L</strong></td>
                            </tr>
                            <tr class="total-row">
                              <td><strong>Annual Recurring</strong></td>
                              <td></td>
                              <td class="cost-value"><strong>₹5.8L</strong></td>
                            </tr>
                          </tbody>
                        </table>
                      </div>

                      <!-- Scenario Analysis -->
                      <div class="cost-section-card scenario-section">
                        <div class="scenario-header">SCENARIO ANALYSIS</div>
                        <table class="scenario-table">
                          <thead>
                            <tr>
                              <th>SCENARIO</th>
                              <th>ANNUAL BENEFIT</th>
                              <th>PAYBACK</th>
                              <th>YEAR 1 NET</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>Conservative (50%)</td>
                              <td class="benefit-value">₹2.9L/yr</td>
                              <td>12 wks</td>
                              <td class="net-value negative">₹-4.1L</td>
                            </tr>
                            <tr>
                              <td>Base Case (P50)</td>
                              <td class="benefit-value">₹5.7L/yr</td>
                              <td>6 wks</td>
                              <td class="net-value negative">₹-1.3L</td>
                            </tr>
                            <tr>
                              <td>Optimistic (P90)</td>
                              <td class="benefit-value">₹7.4L/yr</td>
                              <td>4 wks</td>
                              <td class="net-value positive">₹0.4L</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>

                      <!-- Action Buttons -->
                      <div class="cost-actions">
                        <button class="btn-project-preview" onclick="goToPlanTab()">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                          Project Preview
                        </button>
                        <button class="btn-approve-execute">
                          Approve & Execute
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"/><path d="M12 5l7 7-7 7"/></svg>
                        </button>
                      </div>
                    </div>

                    <!-- Right: Return Summary -->
                    <div class="return-summary-sidebar">
                      <div class="return-summary-card">
                        <div class="return-summary-header">
                          <span class="return-icon">📊</span>
                          <span class="return-title">RETURN SUMMARY</span>
                        </div>
                        <div class="return-metrics">
                          <div class="return-metric-item">
                            <div class="return-metric-value">₹7.0L</div>
                            <div class="return-metric-label">TOTAL INVESTMENT</div>
                          </div>
                          <div class="return-metric-item">
                            <div class="return-metric-value highlight">₹4.8L/mo</div>
                            <div class="return-metric-label">MONTHLY BENEFIT (REV + SAVINGS)</div>
                          </div>
                          <div class="return-metric-item">
                            <div class="return-metric-value highlight">6 Weeks</div>
                            <div class="return-metric-label">PAYBACK PERIOD</div>
                          </div>
                          <div class="return-metric-item">
                            <div class="return-metric-value highlight">₹3.8L</div>
                            <div class="return-metric-label">REVENUE GAIN / MONTH</div>
                          </div>
                          <div class="return-metric-item">
                            <div class="return-metric-value highlight">₹95,000</div>
                            <div class="return-metric-label">COST SAVING / MONTH</div>
                          </div>
                          <div class="return-metric-item">
                            <div class="return-metric-value highlight">+₹68L/yr</div>
                            <div class="return-metric-label">EBITDA IMPACT</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="tab-content" id="tab-project">
                  <div class="project-content-layout">
                    <!-- Project Sub-tabs Navigation -->
                    <div class="project-subtabs">
                      <button class="project-subtab-btn active" data-subtab="gantt">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                        Gantt Chart
                      </button>
                      <button class="project-subtab-btn" data-subtab="kpi">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/></svg>
                        KPI Monitoring
                      </button>
                      <button class="project-subtab-btn" data-subtab="resources">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                        Resources
                      </button>
                      <button class="project-subtab-btn" data-subtab="ebitda">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                        EBITDA Projection
                      </button>
                    </div>

                    <!-- Gantt Chart Sub-tab -->
                    <div class="project-subtab-content active" id="subtab-gantt">
                      <div class="gantt-section">
                        <div class="gantt-header">
                          <h3>Full Implementation Gantt — Week 1 to Week 52</h3>
                          <div class="gantt-legend">
                            <span class="legend-item"><span class="legend-dot" style="background:#3b82f6"></span>P1 OT</span>
                            <span class="legend-item"><span class="legend-dot" style="background:#06b6d4"></span>P2 ICU</span>
                            <span class="legend-item"><span class="legend-dot" style="background:#8b5cf6"></span>P3 Margin</span>
                            <span class="legend-item"><span class="legend-dot" style="background:#f59e0b"></span>P4 Cash</span>
                            <span class="legend-item"><span class="legend-dot" style="background:#ef4444"></span>P5 Nursing</span>
                            <span class="legend-item"><span class="legend-dot" style="background:#22c55e"></span>P6 Pharmacy</span>
                            <span class="legend-item"><span class="legend-dot" style="background:#ec4899"></span>AI-P1</span>
                            <span class="legend-item"><span class="legend-dot" style="background:#14b8a6"></span>AI-P2</span>
                            <span class="legend-item"><span class="legend-dot" style="background:#a855f7"></span>AI-P3</span>
                            <span class="legend-item"><span class="legend-dot milestone"></span>Milestone</span>
                          </div>
                        </div>
                        
                        <div class="gantt-phases">
                          <div class="phase-label phase-1">PHASE 1: QUICK WINS (W1-8)</div>
                          <div class="phase-label phase-2">PHASE 2: CORE SYSTEMS (W9-18)</div>
                          <div class="phase-label phase-3">PHASE 3: STABILISE (W17-26)</div>
                          <div class="phase-label phase-4">PHASE 4: OPTIMISE & SUSTAIN (W27-52)</div>
                        </div>

                        <div class="gantt-chart-container">
                          <table class="gantt-table">
                            <thead>
                              <tr>
                                <th class="col-intervention">INTERVENTION</th>
                                <th class="col-weeks" colspan="52">
                                  <div class="week-numbers">
                                    <span>4</span><span>8</span><span>12</span><span>16</span><span>20</span><span>24</span><span>28</span><span>32</span><span>36</span><span>40</span><span>44</span><span>48</span><span>52</span>
                                  </div>
                                </th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr class="gantt-row" data-delay="0.1">
                                <td class="intervention-cell">
                                  <span class="problem-tag ai-p2">AI-P2</span>
                                  <div class="intervention-text">Hire biomedical engineer + backlog clearance sprint</div>
                                  <div class="intervention-owner">Admin + External Engineer</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 0%; width: 12%; background: #14b8a6;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.15">
                                <td class="intervention-cell">
                                  <span class="problem-tag p1">P1</span>
                                  <div class="intervention-text">48hr + 2hr pre-op equipment checklist in HIS</div>
                                  <div class="intervention-owner">IT Team</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 2%; width: 8%; background: #3b82f6;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.2">
                                <td class="intervention-cell">
                                  <span class="problem-tag p2">P2</span>
                                  <div class="intervention-text">Dawn Protocol pilot (3 consultants)</div>
                                  <div class="intervention-owner">Dr. Mehta</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 4%; width: 10%; background: #06b6d4;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.25">
                                <td class="intervention-cell">
                                  <span class="problem-tag p6">P6</span>
                                  <div class="intervention-text">Medical Committee: Generic formulary approval</div>
                                  <div class="intervention-owner">Dr. Mehta + Med Committee</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 4%; width: 6%; background: #22c55e;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.3">
                                <td class="intervention-cell">
                                  <span class="problem-tag p5">P5</span>
                                  <div class="intervention-text">Agency nurse 4hr ICU orientation + PPH countersigning rule</div>
                                  <div class="intervention-owner">Nursing Superintendent</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 2%; width: 8%; background: #ef4444;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.35">
                                <td class="intervention-cell">
                                  <span class="problem-tag p4">P4</span>
                                  <div class="intervention-text">TPA claims tracker + assign TPA executive role</div>
                                  <div class="intervention-owner">Billing Head</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 0%; width: 4%; background: #f59e0b;"></div>
                                  <div class="gantt-bar" style="left: 6%; width: 6%; background: #f59e0b;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.4">
                                <td class="intervention-cell">
                                  <span class="problem-tag ai-p3">AI-P3</span>
                                  <div class="intervention-text">Counsellor incentive redesign (Dr. Mehta personal communication)</div>
                                  <div class="intervention-owner">Dr. Mehta + HR</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 4%; width: 10%; background: #a855f7;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.45">
                                <td class="intervention-cell">
                                  <span class="problem-tag p2">P2</span>
                                  <div class="intervention-text">HIS pharmacy par-level + auto-reorder system</div>
                                  <div class="intervention-owner">Pharmacy Head + IT</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 10%; width: 12%; background: #06b6d4;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.5">
                                <td class="intervention-cell">
                                  <span class="problem-tag p2">P2</span>
                                  <div class="intervention-text">HDU conversion (2 beds)</div>
                                  <div class="intervention-owner">Admin + Civil</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 12%; width: 14%; background: #06b6d4;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.55">
                                <td class="intervention-cell">
                                  <span class="problem-tag p2">P2</span>
                                  <div class="intervention-text">ICU step-down protocol in HIS</div>
                                  <div class="intervention-owner">IT + Intensivist</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 14%; width: 10%; background: #06b6d4;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.6">
                                <td class="intervention-cell">
                                  <span class="problem-tag p1">P1</span>
                                  <div class="intervention-text">HIS OT scheduling module activation</div>
                                  <div class="intervention-owner">IT Team</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 16%; width: 8%; background: #3b82f6;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row milestone-row" data-delay="0.65">
                                <td class="intervention-cell milestone-cell">
                                  <span class="problem-tag milestone">ALL</span>
                                  <div class="intervention-text">★ MILESTONE: Month 3 Review — Baselines set, Quick Wins measured</div>
                                  <div class="intervention-owner">Dr. Mehta + Virevo</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="milestone-marker" style="left: 23%;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.7">
                                <td class="intervention-cell">
                                  <span class="problem-tag p5">P5</span>
                                  <div class="intervention-text">Permanent nurse hiring — Phase 1 (6 nurses/month × 3 months)</div>
                                  <div class="intervention-owner">HR Head</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 24%; width: 24%; background: #ef4444;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.75">
                                <td class="intervention-cell">
                                  <span class="problem-tag p3">P3</span>
                                  <div class="intervention-text">Cardiology specialist formalisation</div>
                                  <div class="intervention-owner">Dr. Mehta</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 28%; width: 8%; background: #8b5cf6;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row milestone-row" data-delay="0.8">
                                <td class="intervention-cell milestone-cell">
                                  <span class="problem-tag milestone">ALL</span>
                                  <div class="intervention-text">★ MILESTONE: Month 6 Review — EBITDA trajectory confirmed</div>
                                  <div class="intervention-owner">Dr. Mehta + Virevo</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="milestone-marker" style="left: 46%;"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row" data-delay="0.85">
                                <td class="intervention-cell">
                                  <span class="problem-tag p3">P3</span>
                                  <div class="intervention-text">Continuous monitoring — all KPIs — adaptive recommendations</div>
                                  <div class="intervention-owner">Virevo Platform</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="gantt-bar" style="left: 46%; width: 54%; background: linear-gradient(90deg, #8b5cf6, #22c55e);"></div>
                                </td>
                              </tr>
                              <tr class="gantt-row milestone-row" data-delay="0.9">
                                <td class="intervention-cell milestone-cell">
                                  <span class="problem-tag milestone">ALL</span>
                                  <div class="intervention-text">★ MILESTONE: Month 12 — EBITDA +₹5.43Cr target</div>
                                  <div class="intervention-owner">Dr. Mehta + Virevo</div>
                                </td>
                                <td class="gantt-bars-cell">
                                  <div class="milestone-marker" style="left: 96%;"></div>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>

                    <!-- KPI Monitoring Sub-tab -->
                    <div class="project-subtab-content" id="subtab-kpi">
                      <div class="kpi-section">
                        <div class="kpi-header">
                          <p><strong>10 new KPIs</strong> added to continuous monitoring. Adaptive recommendation triggered if actuals deviate from trajectory.</p>
                        </div>
                        <div class="kpi-cards-grid">
                          <div class="kpi-card" data-delay="0.1">
                            <div class="kpi-card-title">OT UTILISATION</div>
                            <div class="kpi-card-base">Base: <strong>58%</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">76%</span></div>
                            <div class="kpi-card-alert">Alert if <65% in Month 3+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.15">
                            <div class="kpi-card-title">OT CANCELLATION RATE</div>
                            <div class="kpi-card-base">Base: <strong>17.3%</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">&lt;6%</span></div>
                            <div class="kpi-card-alert">Alert if >12% in Month 2+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.2">
                            <div class="kpi-card-title">ICU LOS</div>
                            <div class="kpi-card-base">Base: <strong>5.8 days</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">3.9 days</span></div>
                            <div class="kpi-card-alert">Alert if >5.0 days in Month 4+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.25">
                            <div class="kpi-card-title">ICU RPOB</div>
                            <div class="kpi-card-base">Base: <strong>₹4,100/day</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">₹5,800/day</span></div>
                            <div class="kpi-card-alert">Alert if <₹4,800 in Month 4+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.3">
                            <div class="kpi-card-title">BED TURNOVER TIME</div>
                            <div class="kpi-card-base">Base: <strong>15.1 hrs</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">6.5 hrs</span></div>
                            <div class="kpi-card-alert">Alert if >10 hrs in Month 3+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.35">
                            <div class="kpi-card-title">WARD ROUND DECISION TIME</div>
                            <div class="kpi-card-base">Base: <strong>11:30 AM avg</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">8:15 AM avg</span></div>
                            <div class="kpi-card-alert">Alert if >9:30 AM daily avg</div>
                          </div>
                          <div class="kpi-card" data-delay="0.4">
                            <div class="kpi-card-title">DRUG COST % REVENUE</div>
                            <div class="kpi-card-base">Base: <strong>23.8%</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">17.5%</span></div>
                            <div class="kpi-card-alert">Alert if >21% in Month 4+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.45">
                            <div class="kpi-card-title">AGENCY NURSING COST/MONTH</div>
                            <div class="kpi-card-base">Base: <strong>₹29.4L</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">₹8L</span></div>
                            <div class="kpi-card-alert">Alert if >₹22L in Month 3+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.5">
                            <div class="kpi-card-title">INSURANCE CLAIM TAT</div>
                            <div class="kpi-card-base">Base: <strong>38 days</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">20 days</span></div>
                            <div class="kpi-card-alert">Alert if >30 days in Month 4+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.55">
                            <div class="kpi-card-title">RECEIVABLES DAYS OUTSTANDING</div>
                            <div class="kpi-card-base">Base: <strong>81 days</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">40 days</span></div>
                            <div class="kpi-card-alert">Alert if >65 days in Month 6+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.6">
                            <div class="kpi-card-title">GENERIC SUBSTITUTION RATE</div>
                            <div class="kpi-card-base">Base: <strong>0%</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">80%</span></div>
                            <div class="kpi-card-alert">Alert if <40% in Month 4+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.65">
                            <div class="kpi-card-title">72-HR RE-ADMISSION RATE</div>
                            <div class="kpi-card-base">Base: <strong>5%</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">&lt;2%</span></div>
                            <div class="kpi-card-alert">Alert if >4% in Month 3+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.7">
                            <div class="kpi-card-title">CARDIOLOGY CASE SHARE</div>
                            <div class="kpi-card-base">Base: <strong>8%</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">15%</span></div>
                            <div class="kpi-card-alert">Alert if <10% in Month 6+</div>
                          </div>
                          <div class="kpi-card" data-delay="0.75">
                            <div class="kpi-card-title">EBITDA %</div>
                            <div class="kpi-card-base">Base: <strong>8.0%</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">13.5%</span></div>
                            <div class="kpi-card-alert">Alert if <10% at Month 6</div>
                          </div>
                          <div class="kpi-card" data-delay="0.8">
                            <div class="kpi-card-title">BEDS PENDING >6HRS</div>
                            <div class="kpi-card-base">Base: <strong>8-12/day avg</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">&lt;2/day</span></div>
                            <div class="kpi-card-alert">Real-time alert per bed</div>
                          </div>
                          <div class="kpi-card" data-delay="0.85">
                            <div class="kpi-card-title">PRE-OP CHECKLIST COMPLIANCE</div>
                            <div class="kpi-card-base">Base: <strong>~0%</strong></div>
                            <div class="kpi-card-target">→ Target: <span class="target-value">>95%</span></div>
                            <div class="kpi-card-alert">Alert if <80% in Month 3+</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Resources Sub-tab -->
                    <div class="project-subtab-content" id="subtab-resources">
                      <div class="resources-section">
                        <div class="resources-table-card">
                          <div class="resources-header">
                            <span class="resources-icon">👥</span>
                            <span class="resources-title">RESOURCE ALLOCATION</span>
                          </div>
                          <table class="resources-table">
                            <thead>
                              <tr>
                                <th class="col-resource">RESOURCE</th>
                                <th class="col-type">TYPE</th>
                                <th class="col-problem">PROBLEM</th>
                                <th class="col-costtype">COST TYPE</th>
                                <th class="col-monthly">MONTHLY (₹)</th>
                                <th class="col-annual">ANNUAL (₹)</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr data-delay="0.1">
                                <td>Part-time Biomedical Engineer</td>
                                <td><span class="resource-type human">Human</span></td>
                                <td><span class="problem-ref ai">AI-P2</span></td>
                                <td><span class="cost-type-badge recurring">Recurring</span></td>
                                <td class="monthly-val">₹18,000</td>
                                <td class="annual-val">₹2.2L</td>
                              </tr>
                              <tr data-delay="0.15">
                                <td>Dedicated TPA Executive</td>
                                <td><span class="resource-type human">Human</span></td>
                                <td><span class="problem-ref p4">P4</span></td>
                                <td><span class="cost-type-badge recurring">Recurring</span></td>
                                <td class="monthly-val">₹20,000</td>
                                <td class="annual-val">₹2.4L</td>
                              </tr>
                              <tr data-delay="0.2">
                                <td>Cardiology Specialist Retainer</td>
                                <td><span class="resource-type human">Human</span></td>
                                <td><span class="problem-ref p3">P3</span></td>
                                <td><span class="cost-type-badge recurring">Recurring</span></td>
                                <td class="monthly-val">₹12,500</td>
                                <td class="annual-val">₹1.5L</td>
                              </tr>
                              <tr data-delay="0.25">
                                <td>ICU Permanent Nurses (18) — Signing Bonus</td>
                                <td><span class="resource-type human">Human</span></td>
                                <td><span class="problem-ref p5">P5</span></td>
                                <td><span class="cost-type-badge onetime">One-time</span></td>
                                <td class="monthly-val">—</td>
                                <td class="annual-val">₹3.6L</td>
                              </tr>
                              <tr data-delay="0.3">
                                <td>ICU Permanent Nurses (18) — Monthly Allowance</td>
                                <td><span class="resource-type human">Human</span></td>
                                <td><span class="problem-ref p5">P5</span></td>
                                <td><span class="cost-type-badge recurring">Recurring</span></td>
                                <td class="monthly-val">₹54,000</td>
                                <td class="annual-val">₹6.5L</td>
                              </tr>
                              <tr data-delay="0.35">
                                <td>ICU/OT Nurse Salary Band Revision</td>
                                <td><span class="resource-type human">Human</span></td>
                                <td><span class="problem-ref p5">P5</span></td>
                                <td><span class="cost-type-badge recurring">Recurring</span></td>
                                <td class="monthly-val">₹90,000</td>
                                <td class="annual-val">₹10.8L</td>
                              </tr>
                              <tr data-delay="0.4">
                                <td>HIS OT Scheduling Module</td>
                                <td><span class="resource-type system">System</span></td>
                                <td><span class="problem-ref p1">P1</span></td>
                                <td><span class="cost-type-badge onetime">One-time</span></td>
                                <td class="monthly-val">—</td>
                                <td class="annual-val">₹80,000</td>
                              </tr>
                              <tr data-delay="0.45">
                                <td>HIS Pharmacy Par-Level + Auto Reorder</td>
                                <td><span class="resource-type system">System</span></td>
                                <td><span class="problem-ref multi">P2/P6</span></td>
                                <td><span class="cost-type-badge onetime">One-time</span></td>
                                <td class="monthly-val">—</td>
                                <td class="annual-val">₹1.2L</td>
                              </tr>
                              <tr data-delay="0.5">
                                <td>HIS ICU Step-Down Workflow</td>
                                <td><span class="resource-type system">System</span></td>
                                <td><span class="problem-ref p2">P2</span></td>
                                <td><span class="cost-type-badge onetime">One-time</span></td>
                                <td class="monthly-val">—</td>
                                <td class="annual-val">₹80,000</td>
                              </tr>
                              <tr data-delay="0.55">
                                <td>HDU Bed Conversion (2 beds)</td>
                                <td><span class="resource-type capital">Capital</span></td>
                                <td><span class="problem-ref p2">P2</span></td>
                                <td><span class="cost-type-badge onetime">One-time</span></td>
                                <td class="monthly-val">—</td>
                                <td class="annual-val">₹3.2L</td>
                              </tr>
                              <tr data-delay="0.6">
                                <td>Linen Buffer Stock (ward-level)</td>
                                <td><span class="resource-type material">Material</span></td>
                                <td><span class="problem-ref p1">P1</span></td>
                                <td><span class="cost-type-badge onetime">One-time</span></td>
                                <td class="monthly-val">—</td>
                                <td class="annual-val">₹45,000</td>
                              </tr>
                              <tr data-delay="0.65">
                                <td>Virevo Platform (Year 1)</td>
                                <td><span class="resource-type service">Service</span></td>
                                <td><span class="problem-ref all">ALL</span></td>
                                <td><span class="cost-type-badge recurring">Recurring</span></td>
                                <td class="monthly-val">₹1.4L</td>
                                <td class="annual-val">₹17.2L</td>
                              </tr>
                            </tbody>
                            <tfoot>
                              <tr class="total-row onetime-total" data-delay="0.7">
                                <td colspan="5"><strong>One-time Total</strong></td>
                                <td class="annual-val"><strong>₹14.3L</strong></td>
                              </tr>
                              <tr class="total-row recurring-total" data-delay="0.75">
                                <td colspan="5"><strong>Annual Recurring Total</strong></td>
                                <td class="annual-val"><strong>₹42.9L</strong></td>
                              </tr>
                              <tr class="total-row grand-total" data-delay="0.8">
                                <td colspan="5"><strong>Total Year 1 Investment</strong></td>
                                <td class="annual-val"><strong>₹57.2L</strong></td>
                              </tr>
                            </tfoot>
                          </table>
                        </div>
                      </div>
                    </div>

                    <!-- EBITDA Projection Sub-tab -->
                    <div class="project-subtab-content" id="subtab-ebitda">
                      <div class="ebitda-section">
                        <div class="ebitda-chart-card">
                          <div class="ebitda-chart-title">EBITDA % TRAJECTORY — MONTH 0 TO MONTH 12 (BASELINE 8.0% → TARGET 13.5%)</div>
                          <div class="ebitda-chart-container">
                            <div class="ebitda-y-axis">
                              <span>15%</span>
                              <span>14%</span>
                              <span>13%</span>
                              <span>12%</span>
                              <span>11%</span>
                              <span>10%</span>
                              <span>9%</span>
                              <span>8%</span>
                            </div>
                            <div class="ebitda-chart-area">
                              <div class="chart-grid-lines">
                                <div class="grid-line"></div>
                                <div class="grid-line"></div>
                                <div class="grid-line"></div>
                                <div class="grid-line"></div>
                                <div class="grid-line"></div>
                                <div class="grid-line"></div>
                                <div class="grid-line"></div>
                                <div class="grid-line"></div>
                              </div>
                              <svg class="ebitda-svg" viewBox="0 0 600 200" preserveAspectRatio="none">
                                <!-- Confidence band -->
                                <path class="confidence-band" d="M0,180 Q100,170 150,150 T300,100 T450,60 T600,30 L600,50 Q450,80 300,120 T150,165 T0,185 Z" fill="rgba(16, 185, 129, 0.15)"/>
                                <!-- P10/P90 dashed lines -->
                                <path class="p90-line" d="M0,175 Q100,165 150,145 T300,95 T450,55 T600,25" stroke="#22c55e" stroke-width="2" stroke-dasharray="5,5" fill="none"/>
                                <path class="p10-line" d="M0,182 Q100,175 150,158 T300,115 T450,75 T600,50" stroke="#22c55e" stroke-width="2" stroke-dasharray="5,5" fill="none"/>
                                <!-- P50 Base Case line -->
                                <path class="p50-line" d="M0,180 Q100,170 150,150 T300,100 T450,60 T600,35" stroke="#0d9488" stroke-width="3" fill="none"/>
                                <!-- Data points -->
                                <circle class="data-point" cx="0" cy="180" r="6" fill="#0d9488"/>
                                <circle class="data-point" cx="46" cy="175" r="5" fill="#0d9488"/>
                                <circle class="data-point" cx="92" cy="168" r="5" fill="#0d9488"/>
                                <circle class="data-point" cx="138" cy="155" r="5" fill="#0d9488"/>
                                <circle class="data-point" cx="184" cy="140" r="5" fill="#0d9488"/>
                                <circle class="data-point" cx="230" cy="125" r="5" fill="#0d9488"/>
                                <circle class="data-point milestone-point" cx="276" cy="110" r="8" fill="#f59e0b"/>
                                <circle class="data-point" cx="322" cy="95" r="5" fill="#0d9488"/>
                                <circle class="data-point" cx="368" cy="80" r="5" fill="#0d9488"/>
                                <circle class="data-point" cx="414" cy="65" r="5" fill="#0d9488"/>
                                <circle class="data-point" cx="460" cy="50" r="5" fill="#0d9488"/>
                                <circle class="data-point" cx="506" cy="40" r="5" fill="#0d9488"/>
                                <circle class="data-point milestone-point" cx="552" cy="35" r="8" fill="#22c55e"/>
                              </svg>
                              <!-- Milestone annotations -->
                              <div class="milestone-annotation month6" style="left: 46%; top: 45%;">
                                <div class="annotation-line"></div>
                                <div class="annotation-label">Month 6<br><span>+₹2.76Cr</span></div>
                              </div>
                              <div class="milestone-annotation month12" style="left: 92%; top: 10%;">
                                <div class="annotation-line"></div>
                                <div class="annotation-label">Month 12<br><span>+₹5.43Cr</span></div>
                              </div>
                              <!-- Legend -->
                              <div class="chart-legend-box">
                                <div class="legend-row"><span class="legend-line solid"></span> P50 — Base Case</div>
                                <div class="legend-row"><span class="legend-line dashed"></span> P10 / P90 Range</div>
                                <div class="legend-row"><span class="legend-area"></span> Confidence Band</div>
                              </div>
                            </div>
                            <div class="ebitda-x-axis">
                              <span>Base</span>
                              <span>M1</span>
                              <span>M2</span>
                              <span>M3</span>
                              <span>M4</span>
                              <span>M5</span>
                              <span>M6</span>
                              <span>M7</span>
                              <span>M8</span>
                              <span>M9</span>
                              <span>M10</span>
                              <span>M11</span>
                              <span>M12</span>
                            </div>
                            <div class="ebitda-x-label">Month</div>
                          </div>
                        </div>

                        <!-- Summary Cards -->
                        <div class="ebitda-summary-cards">
                          <div class="ebitda-summary-card" data-delay="0.1">
                            <div class="summary-value investment">₹18.1L</div>
                            <div class="summary-label">TOTAL INVESTMENT</div>
                            <div class="summary-sublabel">all 18 interventions</div>
                          </div>
                          <div class="ebitda-summary-card" data-delay="0.2">
                            <div class="summary-value positive">+₹2.76Cr</div>
                            <div class="summary-label">EBITDA AT MONTH 6</div>
                            <div class="summary-sublabel">P50 projection</div>
                          </div>
                          <div class="ebitda-summary-card" data-delay="0.3">
                            <div class="summary-value positive">+₹5.43Cr</div>
                            <div class="summary-label">EBITDA AT MONTH 12</div>
                            <div class="summary-sublabel">P50 projection</div>
                          </div>
                          <div class="ebitda-summary-card" data-delay="0.4">
                            <div class="summary-value roi">27.2×</div>
                            <div class="summary-label">ROI</div>
                            <div class="summary-sublabel">on total investment</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;

        // Initialize interactive behaviors
        initializeAnalysisInteractions();
      }

      // Toggle node detail - make global
      window.toggleNodeDetail = function(nodeId) {
        const node = document.getElementById(`node-${nodeId}`);
        const detail = document.getElementById(`detail-${nodeId}`);
        
        if (node && detail) {
          node.classList.toggle('expanded');
          detail.classList.toggle('expanded');
        }
      }

      // Toggle dropdown - make global
      window.toggleDropdown = function(dropdownId) {
        const header = document.querySelector(`#${dropdownId} .dropdown-header`);
        const content = document.getElementById(`content-${dropdownId}`);
        
        header.classList.toggle('expanded');
        content.classList.toggle('expanded');
      }

      // Toggle cause tree - make global
      window.toggleCause = function(causeNum) {
        const causeItem = document.querySelector(`[onclick="toggleCause(${causeNum})"]`);
        const treeContainer = document.getElementById(`tree-cause-${causeNum}`);
        
        causeItem.classList.toggle('expanded');
        treeContainer.classList.toggle('expanded');
      }

      // Mitigation Actions Logic
      window.checkMitigationApprovals = function() {
        const checkboxes = document.querySelectorAll('.mitigation-approval-checkbox');
        const btn = document.getElementById('btn-final-approve');
        
        let anyChecked = false;
        checkboxes.forEach(cb => {
          if (cb.checked) anyChecked = true;
        });
        
        if (btn) {
          btn.disabled = !anyChecked;
        }
      };

      window.approveAndGoToCost = function() {
        const costTabBtn = document.querySelector('.tab-btn[data-tab="cost"]');
        if (costTabBtn) {
          // Collapse mitigation dropdown
          const mitigationDropdown = document.getElementById('dropdown-mitigation');
          if (mitigationDropdown) {
             const header = mitigationDropdown.querySelector('.dropdown-header');
             const content = document.getElementById('content-dropdown-mitigation');
             header.classList.remove('expanded');
             content.classList.remove('expanded');
          }
          
          costTabBtn.click();
        }
      };

      window.goToPlanTab = function() {
        const projectTabBtn = document.querySelector('.tab-btn[data-tab="project"]');
        if (projectTabBtn) {
          projectTabBtn.click();
        }
      };

      // Dashboard Data for Problems
      const problemData = {
        "1": { 
          header: "P1 &middot; OT Utilisation", 
          title: "P1 — OT Utilisation Fluctuation", 
          subtitle: "OT Utilisation &middot; Baseline: 58% &rarr; Target: 76%", 
          impact: "+₹68L/yr", 
          baseline: "58", 
          target: "76", 
          actual: "71.4",
          decimals: 1,
          suffix: "%"
        },
        "2": { 
          header: "P2 &middot; ICU Revenue", 
          title: "P2 — ICU Revenue Leakage", 
          subtitle: "ICU Revenue &middot; Baseline: ₹1.2Cr &rarr; Target: ₹1.8Cr", 
          impact: "+₹72L/yr", 
          baseline: "1.2", 
          target: "1.8", 
          actual: "1.4",
          decimals: 1,
          suffix: "Cr"
        },
        "3": { 
          header: "P3 &middot; Margins", 
          title: "P3 — Operational Margins Drop", 
          subtitle: "EBITDA Margins &middot; Baseline: 12% &rarr; Target: 18%", 
          impact: "+₹1.5Cr/yr", 
          baseline: "12", 
          target: "18", 
          actual: "14",
          decimals: 0,
          suffix: "%"
        },
        "4": { 
          header: "P4 &middot; Cash Flow", 
          title: "P4 — Delayed Cash Flow Collection", 
          subtitle: "Days Sales Outstanding &middot; Baseline: 65 Days &rarr; Target: 45 Days", 
          impact: "+₹90L/yr", 
          baseline: "65", 
          target: "45", 
          actual: "58",
          decimals: 0,
          suffix: ""
        },
        "5": { 
          header: "P5 &middot; Agency Nursing", 
          title: "P5 — High Agency Nursing Costs", 
          subtitle: "Agency Mix &middot; Baseline: 35% &rarr; Target: 15%", 
          impact: "+₹45L/yr", 
          baseline: "35", 
          target: "15", 
          actual: "28",
          decimals: 0,
          suffix: "%"
        },
        "6": { 
          header: "P6 &middot; Pharmacy Cost", 
          title: "P6 — Pharmacy Inventory Wastage", 
          subtitle: "Wastage Rate &middot; Baseline: 8% &rarr; Target: 3%", 
          impact: "+₹30L/yr", 
          baseline: "8", 
          target: "3", 
          actual: "6",
          decimals: 0,
          suffix: "%"
        },
        "7": { 
          header: "AI-P1 &middot; Ward Round Timing", 
          title: "AI-P1 — Inconsistent Ward Round Timing", 
          subtitle: "Avg Round Delay &middot; Baseline: 120 mins &rarr; Target: 30 mins", 
          impact: "+₹20L/yr", 
          baseline: "120", 
          target: "30", 
          actual: "90",
          decimals: 0,
          suffix: ""
        },
        "8": { 
          header: "AI-P2 &middot; Biomedical Maintenance", 
          title: "AI-P2 — Biomedical Equipment Downtime", 
          subtitle: "Equip Downtime &middot; Baseline: 15% &rarr; Target: 5%", 
          impact: "+₹85L/yr", 
          baseline: "15", 
          target: "5", 
          actual: "11",
          decimals: 0,
          suffix: "%"
        },
        "9": { 
          header: "AI-P3 &middot; Counsellor Incentives", 
          title: "AI-P3 — Misaligned Counsellor Incentives", 
          subtitle: "Conversion Rate &middot; Baseline: 22% &rarr; Target: 40%", 
          impact: "+₹50L/yr", 
          baseline: "22", 
          target: "40", 
          actual: "28",
          decimals: 0,
          suffix: "%"
        }
      };

      // Counter animation logic
      window.animateCounters = function(forceReset = false) {
        document.querySelectorAll('.counter-animate').forEach(counter => {
          const target = parseFloat(counter.getAttribute('data-target')) || 0;
          const suffix = counter.getAttribute('data-suffix') !== null ? counter.getAttribute('data-suffix') : '%';
          const decimals = parseInt(counter.getAttribute('data-decimals')) || 0;
          const duration = 2000; // ms for a slower, smoother animation
          
          let startValue = forceReset ? 0 : parseFloat(counter.innerText) || 0;
          
          // Only animate if there's a difference
          if (Math.abs(startValue - target) < 0.1 && !forceReset) {
            counter.innerText = target.toFixed(decimals) + suffix;
            return;
          }
          
          if(counter.animationTimer) cancelAnimationFrame(counter.animationTimer);
          
          const startTime = performance.now();
          const difference = target - startValue;
          
          // Ensure initial state is rendered
          counter.innerText = startValue.toFixed(decimals) + suffix;
          
          const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // easeOutCubic giving a very smooth deceleration
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            
            const nextValue = startValue + (difference * easeProgress);
            counter.innerText = nextValue.toFixed(decimals) + suffix;
            
            if (progress < 1) {
              counter.animationTimer = requestAnimationFrame(animate);
            } else {
              counter.innerText = target.toFixed(decimals) + suffix;
            }
          };
          
          counter.animationTimer = requestAnimationFrame(animate);
        });
      };

      // Function to map data to problem UI
      window.updateProblemDashboard = function(problemId) {
        const data = problemData[problemId];
        if (!data) return;
        
        // Update headers
        const mainHeader = document.getElementById('problem-statement-title');
        if (mainHeader) mainHeader.innerHTML = `Problem Statement & Causes : ${data.header}`;
        
        document.getElementById('dashboard-main-title').innerHTML = data.title;
        document.getElementById('dashboard-subtitle').innerHTML = data.subtitle;
        document.getElementById('dashboard-impact-value').innerHTML = data.impact;
        
        // Set counter targets
        const bLine = document.getElementById('dashboard-baseline');
        const tgt = document.getElementById('dashboard-target');
        const act = document.getElementById('dashboard-actual');
        
        bLine.setAttribute('data-target', data.baseline);
        tgt.setAttribute('data-target', data.target);
        act.setAttribute('data-target', data.actual);
        
        bLine.setAttribute('data-decimals', data.decimals);
        tgt.setAttribute('data-decimals', data.decimals);
        act.setAttribute('data-decimals', data.decimals);
        
        const sf = data.suffix !== undefined ? data.suffix : '%';
        bLine.setAttribute('data-suffix', sf);
        tgt.setAttribute('data-suffix', sf);
        act.setAttribute('data-suffix', sf);
        
        // Retrigger animation
        animateCounters(true);
      };

      // Initialize interactive behaviors
      function initializeAnalysisInteractions() {
        // Problem buttons
        document.querySelectorAll('.problem-btn').forEach(btn => {
          btn.addEventListener('click', () => {
            document.querySelectorAll('.problem-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            updateProblemDashboard(btn.dataset.problem);
          });
        });

        // Tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
          btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(`tab-${tab}`).classList.add('active');
            
            // If switching to project tab, animate gantt bars
            if (tab === 'project') {
              setTimeout(() => animateGanttBars(), 200);
            }
          });
        });

        // Project Sub-tab buttons
        document.querySelectorAll('.project-subtab-btn').forEach(btn => {
          btn.addEventListener('click', () => {
            const subtab = btn.dataset.subtab;
            
            document.querySelectorAll('.project-subtab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.project-subtab-content').forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            const target = document.getElementById(`subtab-${subtab}`);
            if (target) target.classList.add('active');
            
            // Animate gantt bars when switching to gantt subtab
            if (subtab === 'gantt') {
              setTimeout(() => animateGanttBars(), 200);
            }
          });
        });

        // Initial animation
        setTimeout(() => {
          animateCounters(true);
          document.querySelectorAll('.percentage-fill').forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
              bar.style.width = width;
            }, 100);
          });
        }, 300);
      }

      // Gantt bar animation
      window.animateGanttBars = function() {
        document.querySelectorAll('.gantt-bar').forEach((bar, index) => {
          const finalWidth = bar.style.width;
          bar.style.width = '0%';
          bar.style.opacity = '0';
          setTimeout(() => {
            bar.style.transition = 'width 1.2s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.6s ease';
            bar.style.width = finalWidth;
            bar.style.opacity = '1';
          }, 80 * index);
        });
        
        document.querySelectorAll('.milestone-marker').forEach((marker, index) => {
          marker.style.opacity = '0';
          marker.style.transform = 'translateX(-50%) scale(0)';
          setTimeout(() => {
            marker.style.transition = 'opacity 0.6s ease, transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
            marker.style.opacity = '1';
            marker.style.transform = 'translateX(-50%) scale(1)';
          }, 200 + 120 * index);
        });
      };


      /* ─────────────────────────────────────────────────
         INITIALIZE ANALYSIS
         ───────────────────────────────────────────────── */
      function initializeAnalysis() {
        if (userQuery) {
          // Show user's original query
          let queryContent = userQuery;
          if (attachments.length > 0) {
            queryContent += `<br><small style="opacity: 0.7;">📎 ${attachments.join(', ')}</small>`;
          }
          addChatMessage('user', queryContent);

          // Show processing status
          addProcessingStatus();

          // Simulate processing steps
          setTimeout(() => {
            updateProcessingStep('step1', true);
          }, 500);

          setTimeout(() => {
            updateProcessingStep('step2', true);
          }, 1000);

          setTimeout(() => {
            updateProcessingStep('step3', true);
          }, 1500);

          setTimeout(() => {
            updateProcessingStep('step4', true);

            // Remove processing status and show result
            setTimeout(() => {
              const processingEl = document.getElementById('processingStatus');
              if (processingEl) processingEl.remove();

              addChatMessage('assistant', `I've completed the analysis of your query. The results are displayed in the main panel. You can see the key metrics, detailed analysis, and processing steps that were performed.<br><br>Feel free to ask any follow-up questions or request more specific information!`);

              // Render analysis results in main area
              renderAnalysisResults(userQuery);

            }, 300);
          }, 2000);

        } else {
          // No query, show empty state
          analysisContent.innerHTML = `
            <div class="empty-analysis">
              <img src="images/Tojo_Namaste.png" alt="Tojo" class="empty-icon">
              <div class="empty-title">Ready to Analyze</div>
              <div class="empty-subtitle">Enter a query in the chat panel to begin analysis, or go back to the home page to start a new conversation.</div>
            </div>
          `;

          addChatMessage('assistant', `Hello ${userName}! I'm ready to help you with any analysis. Type your question or paste some data, and I'll provide insights and results.`);
        }
      }

      initializeAnalysis();


      /* ─────────────────────────────────────────────────
         CHAT INPUT FUNCTIONALITY
         ───────────────────────────────────────────────── */
      const chatInput = document.getElementById('chatInput');
      const sendChatBtn = document.getElementById('sendChatBtn');

      // Auto-resize textarea
      chatInput.addEventListener('input', () => {
        chatInput.style.height = 'auto';
        chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
      });

      function handleSendChat() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message
        addChatMessage('user', message);

        // Clear input
        chatInput.value = '';
        chatInput.style.height = 'auto';

        // Simulate AI response
        setTimeout(() => {
          addChatMessage('assistant', `Thank you for your follow-up question. Based on my analysis, I can provide additional insights on "${message.substring(0, 50)}${message.length > 50 ? '...' : ''}"<br><br>Would you like me to dive deeper into any specific aspect of this analysis?`);
        }, 1000);
      }

      sendChatBtn.addEventListener('click', handleSendChat);

      chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          handleSendChat();
        }
      });


      /* ─────────────────────────────────────────────────
         VOICE RECORDING FUNCTIONALITY
         ───────────────────────────────────────────────── */
      const voiceBtn = document.getElementById('voiceBtn');
      
      if (voiceBtn && chatInput) {
        // Check for browser support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (SpeechRecognition) {
          const recognition = new SpeechRecognition();
          let isRecording = false;
          
          // Configure recognition
          recognition.continuous = true;
          recognition.interimResults = true;
          recognition.lang = 'en-US';
          
          // Store the text before starting (to append to it)
          let previousText = '';
          
          voiceBtn.addEventListener('click', () => {
            if (isRecording) {
              // Stop recording
              recognition.stop();
              isRecording = false;
              voiceBtn.classList.remove('recording');
              voiceBtn.title = 'Record Voice';
            } else {
              // Start recording
              previousText = chatInput.value;
              recognition.start();
              isRecording = true;
              voiceBtn.classList.add('recording');
              voiceBtn.title = 'Stop Recording';
              
              // Show visual feedback
              showVoiceNotification('Listening... Speak now');
            }
          });
          
          recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
              const transcript = event.results[i][0].transcript;
              if (event.results[i].isFinal) {
                finalTranscript += transcript;
              } else {
                interimTranscript += transcript;
              }
            }
            
            // Update textarea with transcribed text
            const separator = previousText && (finalTranscript || interimTranscript) ? ' ' : '';
            chatInput.value = previousText + separator + (finalTranscript || interimTranscript);
            
            // Trigger input event for auto-resize
            chatInput.dispatchEvent(new Event('input'));
            
            // Update previousText when we get final results
            if (finalTranscript) {
              previousText = chatInput.value;
            }
          };
          
          recognition.onend = () => {
            if (isRecording) {
              // Restart if still in recording mode (continuous recognition)
              recognition.start();
            } else {
              showVoiceNotification('Recording stopped');
            }
          };
          
          recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            isRecording = false;
            voiceBtn.classList.remove('recording');
            voiceBtn.title = 'Record Voice';
            
            if (event.error === 'no-speech') {
              showVoiceNotification('No speech detected. Try again.');
            } else if (event.error === 'audio-capture') {
              showVoiceNotification('Microphone not found. Please check your device.');
            } else if (event.error === 'not-allowed') {
              showVoiceNotification('Microphone access denied. Please allow microphone access.');
            } else {
              showVoiceNotification('Voice recognition error. Please try again.');
            }
          };
          
        } else {
          // Browser doesn't support Speech Recognition
          voiceBtn.addEventListener('click', () => {
            showVoiceNotification('Voice recognition is not supported in this browser. Please use Chrome or Edge.');
          });
        }
      }
      
      // Voice notification helper
      function showVoiceNotification(message) {
        // Remove existing notification if any
        const existingNotification = document.querySelector('.voice-notification');
        if (existingNotification) {
          existingNotification.remove();
        }
        
        // Create notification
        const notification = document.createElement('div');
        notification.className = 'voice-notification';
        notification.innerHTML = `
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 1C10.8954 1 10 1.89543 10 3V12C10 13.1046 10.8954 14 12 14C13.1046 14 14 13.1046 14 12V3C14 1.89543 13.1046 1 12 1Z"/>
            <path d="M5 10V12C5 15.866 8.13401 19 12 19C15.866 19 19 15.866 19 12V10"/>
          </svg>
          <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        requestAnimationFrame(() => {
          notification.classList.add('show');
        });
        
        // Remove after delay
        setTimeout(() => {
          notification.classList.remove('show');
          setTimeout(() => notification.remove(), 300);
        }, 2500);
      }


      /* ─────────────────────────────────────────────────
         HOME BUTTON - CLEAR SESSION
         ───────────────────────────────────────────────── */
      const homeNavBtn = document.getElementById('homeNavBtn');
      if (homeNavBtn) {
        homeNavBtn.addEventListener('click', (e) => {
          // Clear query but keep session logged in
          sessionStorage.removeItem('virevo-query');
          sessionStorage.removeItem('virevo-attachments');
        });
      }

    });
