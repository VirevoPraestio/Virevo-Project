document.addEventListener('DOMContentLoaded', () => {

  /* ─────────────────────────────────────────────────
     PAGE-LOAD ANIMATION
     Hide main simulation content until chat loading completes
     ───────────────────────────────────────────────── */
  const simContainer = document.getElementById('virevo-sim-container');
  if (simContainer) {
    simContainer.style.opacity = '0';
    simContainer.style.transition = 'opacity 0.5s ease';
  }

  /* ─────────────────────────────────────────────────
     COLLAPSIBLE CHAT
     ───────────────────────────────────────────────── */
  const chatCollapseBtn = document.getElementById('chatCollapseBtn');
  const chatExpandBtn = document.getElementById('chatExpandBtn');
  const chatPanel = document.querySelector('.chat-panel');
  const analysisMain = document.querySelector('.analysis-main');
  
  const toggleChat = () => {
    chatPanel.classList.toggle('collapsed');
    analysisMain.classList.toggle('expanded');
    if (chatExpandBtn) {
      chatExpandBtn.style.display = chatPanel.classList.contains('collapsed') ? 'flex' : 'none';
    }
  };

  if (chatCollapseBtn && chatPanel) {
    chatCollapseBtn.addEventListener('click', toggleChat);
  }
  if (chatExpandBtn && chatPanel) {
    chatExpandBtn.addEventListener('click', toggleChat);
  }

  /* ─────────────────────────────────────────────────
     THEME SWITCHING (inheriting from analysis.html structure)
     ───────────────────────────────────────────────── */
  const themeBtn = document.getElementById('themeBtn');
  const themeDD = document.getElementById('themeDropdown');
  const themeWrapper = document.getElementById('themeWrapper');

  const savedTheme = localStorage.getItem('virevo-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  document.querySelectorAll('.theme-option').forEach(o => {
    o.classList.toggle('active', o.dataset.theme === savedTheme);
  });

  if (themeBtn) {
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
  }

  /* ─────────────────────────────────────────────────
     TOJO CONVERSATION ENGINE FOR SIMULATION PAGE
     Based on Conversation_Script.md
     ───────────────────────────────────────────────── */
  const tojoSimConversation = {
    state: 'UPLOAD_READY',
    
    responses: {
      uploadIntro: `Great! You're now in the **Upload section**. Here's what you need to do:

**Step 1 — Upload CSV Files**

Drop your hospital's data files in the upload area above. The system needs:
– **HIS / eHospital exports** (patient records, admissions, discharges)
– **Billing data** (Meddoc or your billing system)
– **HR records** (GreytHR or equivalent — staff, shifts, payroll)
– **Pharmacy inventory** (stock movements, dispensing logs)
– **Accounts** (Tally GL exports if available)
– **Biomedical logs** (equipment maintenance, downtime)

The Agent will ingest these and build the retrospective baseline. Once uploaded, I'll guide you through target setting and simulation.

**Drag & drop your files above, or click to browse.**`,

      uploadHelp: `To upload your data:
1. **Drag and drop** CSV files directly onto the upload zone above
2. Or **click the upload area** to browse your files
3. You can upload multiple files at once

Supported formats: CSV, Excel (xlsx), and common data exports from hospital systems.

Need help preparing your data? I can guide you through the format requirements.`,

      targetIntro: `Excellent! Files uploaded successfully. Now let's move to **Step 2 — Target Selection**.

You'll see the parameters the Agent has identified from your data. Select which ones you want to optimize:
– **Required targets** (green) — core metrics like EBITDA, revenue, occupancy
– **Recommended targets** (gold) — high-impact levers the Agent flagged
– **Optional targets** (purple) — additional parameters you can include

Select at least 3 targets to proceed. The Agent will calculate achievable improvements and costs for each.`,

      simulationIntro: `Perfect. Targets locked in. Now we're at **Step 3 — Simulation**.

The Virevo CEO Agent is now running scenarios. For each parameter, you'll see:
– **Current value** — where you are today
– **Achievable target** — what's realistic with standard interventions
– **Dream target** — the stretch goal if you're willing to invest more

Review the costs (capex + opex) and approve the targets you want to pursue. Once you've approved your selection, we'll freeze the plan and move to implementation.`,

      analysisIntro: `The simulation is complete. Let me take you to **Analysis** where you can see the detailed breakdown:
– Root cause trees for each problem
– Intervention recommendations
– Cost-benefit analysis
– Implementation timeline

Ready to dive deeper?`,

      fallback: `I'm here to help you through the simulation process. You can:
– **Upload files** by dragging them to the upload zone
– **Ask questions** about any step
– **Request guidance** on data preparation

What would you like to know?`
    },
    
    processMessage(text) {
      const t = text.toLowerCase();
      
      // Upload-related queries
      if (/how (do|can|should) (i|we) upload/i.test(text) ||
          /upload (help|guide|how)/i.test(text) ||
          /what (files?|data|format)/i.test(text) ||
          /drag.*(drop|file)/i.test(text)) {
        return this.responses.uploadHelp;
      }
      
      // Where to upload
      if (/where.*(upload|put|drop)/i.test(text) ||
          /upload.*(where|area|zone)/i.test(text)) {
        return this.responses.uploadIntro;
      }
      
      // Target-related queries
      if (/target/i.test(text) || /parameter/i.test(text) ||
          /what (do|should) (i|we) (select|choose|pick)/i.test(text)) {
        return this.responses.targetIntro;
      }
      
      // Simulation queries
      if (/simulation/i.test(text) || /scenario/i.test(text) ||
          /run.*(model|simulation)/i.test(text)) {
        return this.responses.simulationIntro;
      }
      
      // Analysis queries
      if (/analysis/i.test(text) || /result/i.test(text) ||
          /root cause/i.test(text) || /finding/i.test(text)) {
        return this.responses.analysisIntro;
      }
      
      // Help/guidance
      if (/help/i.test(text) || /guide/i.test(text) ||
          /what (do|should|can) (i|we)/i.test(text) ||
          /next/i.test(text) || /start/i.test(text)) {
        // Check current page state
        const pageUpload = document.getElementById('pageUpload');
        const pageTargets = document.getElementById('pageTargets');
        const pageSim = document.getElementById('pageSim');
        
        if (pageUpload && pageUpload.classList.contains('active')) {
          return this.responses.uploadIntro;
        } else if (pageTargets && pageTargets.classList.contains('active')) {
          return this.responses.targetIntro;
        } else if (pageSim && pageSim.classList.contains('active')) {
          return this.responses.simulationIntro;
        }
        return this.responses.uploadIntro;
      }
      
      // Greetings
      if (/^(hi|hello|hey|good morning|good afternoon)/i.test(text)) {
        return `Hello! I'm **Tojo**, guiding you through the Virevo simulation. ${this.responses.uploadIntro}`;
      }
      
      return this.responses.fallback;
    }
  };

  /* ─────────────────────────────────────────────────
     CHAT PROCESS LOADING
     ───────────────────────────────────────────────── */
  const userQuery = sessionStorage.getItem('virevo-query') || '';
  const uploadRedirect = sessionStorage.getItem('virevo-upload-redirect');
  const redirectUserQuery = sessionStorage.getItem('virevo-user-query') || '';
  const chatMessagesArea = document.getElementById('chatMessagesArea');
  const chatInput = document.getElementById('chatInput');
  const sendChatBtn = document.getElementById('sendChatBtn');

  function addChatMessage(type, content, time) {
    const msg = document.createElement('div');
    msg.className = `chat-msg ${type}`;
    msg.innerHTML = `
      <div class="msg-bubble">${content.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>')}</div>
      <div class="msg-time">${time || new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
    `;
    if(chatMessagesArea) chatMessagesArea.appendChild(msg);
    if(chatMessagesArea) chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight;
    return msg;
  }

  function showTypingIndicator() {
    const typing = document.createElement('div');
    typing.className = 'chat-msg assistant typing';
    typing.id = 'typingIndicator';
    typing.innerHTML = `
      <div class="typing-indicator">
        <span></span><span></span><span></span>
      </div>
    `;
    if(chatMessagesArea) chatMessagesArea.appendChild(typing);
    if(chatMessagesArea) chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight;
    return typing;
  }

  function addProcessingStatus() {
    const status = document.createElement('div');
    status.className = 'chat-msg assistant';
    status.id = 'processingStatus';
    status.innerHTML = `
      <div class="processing-status">
        <div class="status-header">
          <div class="spinner-mini"></div>
          <span>Setting up Simulation Engine...</span>
        </div>
        <div class="status-item" id="step1">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
          Initializing workspace
        </div>
        <div class="status-item" id="step2">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
          Loading simulation modules
        </div>
        <div class="status-item" id="step3">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
          Preparing data pipelines
        </div>
        <div class="status-item" id="step4">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
          Rendering interface
        </div>
      </div>
    `;
    if(chatMessagesArea) chatMessagesArea.appendChild(status);
    if(chatMessagesArea) chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight;
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

  function revealSimContent() {
    if (simContainer) {
      simContainer.style.opacity = '1';
    }
  }

  /* ─────────────────────────────────────────────────
     CHAT SEND FUNCTIONALITY
     ───────────────────────────────────────────────── */
  function handleSendChat() {
    if (!chatInput) return;
    const message = chatInput.value.trim();
    if (!message) return;
    
    // Add user message
    addChatMessage('user', message);
    chatInput.value = '';
    
    // Show typing indicator
    const typing = showTypingIndicator();
    
    // Get response after delay
    setTimeout(() => {
      if (typing) typing.remove();
      const response = tojoSimConversation.processMessage(message);
      addChatMessage('assistant', response);
    }, 600 + Math.random() * 500);
  }

  if (sendChatBtn) {
    sendChatBtn.addEventListener('click', handleSendChat);
  }
  if (chatInput) {
    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendChat();
      }
    });
  }

  /* ─────────────────────────────────────────────────
     VOICE RECORDING FOR SIMULATION CHAT
     ───────────────────────────────────────────────── */
  const voiceBtn = document.getElementById('voiceBtn');
  
  if (voiceBtn && chatInput) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      let isRecording = false;
      let previousText = '';
      
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';
      
      voiceBtn.addEventListener('click', () => {
        if (isRecording) {
          recognition.stop();
          isRecording = false;
          voiceBtn.classList.remove('recording');
        } else {
          previousText = chatInput.value;
          recognition.start();
          isRecording = true;
          voiceBtn.classList.add('recording');
          showVoiceNotification('Listening... Speak now');
        }
      });
      
      recognition.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }
        
        const separator = previousText && (finalTranscript || interimTranscript) ? ' ' : '';
        chatInput.value = previousText + separator + (finalTranscript || interimTranscript);
        
        if (finalTranscript) {
          previousText = chatInput.value;
        }
      };
      
      recognition.onend = () => {
        if (isRecording) {
          recognition.start();
        } else {
          showVoiceNotification('Recording stopped');
        }
      };
      
      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        isRecording = false;
        voiceBtn.classList.remove('recording');
        showVoiceNotification('Voice recognition error');
      };
    }
  }
  
  function showVoiceNotification(message) {
    const existing = document.querySelector('.voice-notification');
    if (existing) existing.remove();
    
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
    requestAnimationFrame(() => notification.classList.add('show'));
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => notification.remove(), 300);
    }, 2500);
  }

  /* ─────────────────────────────────────────────────
     INITIAL LOAD HANDLING
     ───────────────────────────────────────────────── */
  // Check if redirected from index.html with upload query
  if (uploadRedirect && chatMessagesArea) {
    sessionStorage.removeItem('virevo-upload-redirect');
    sessionStorage.removeItem('virevo-user-query');
    
    // Show the user's original query
    if (redirectUserQuery) {
      addChatMessage('user', redirectUserQuery);
    }
    
    // Show Tojo's response about upload
    setTimeout(() => {
      addChatMessage('assistant', tojoSimConversation.responses.uploadIntro);
      revealSimContent();
    }, 500);
    
  } else if (userQuery && chatMessagesArea) {
    // Regular query flow
    addChatMessage('user', userQuery);
    addProcessingStatus();
    sessionStorage.removeItem('virevo-query');

    // Step-by-step reveal with loading animation
    setTimeout(() => updateProcessingStep('step1', true), 800);
    setTimeout(() => updateProcessingStep('step2', true), 1600);
    setTimeout(() => updateProcessingStep('step3', true), 2500);
    setTimeout(() => {
      updateProcessingStep('step4', true);
      const headerSpinner = document.querySelector('.status-header .spinner-mini');
      if (headerSpinner) {
        headerSpinner.style.display = 'none';
        headerSpinner.nextElementSibling.textContent = 'Setup Complete';
      }
      addChatMessage('assistant', 'Simulation Engine is ready. Upload your CSV data to begin.');
      // Reveal the main simulation content after loading completes
      revealSimContent();
    }, 3200);
  } else {
    // No query — reveal content immediately
    revealSimContent();
  }


  /* ─────────────────────────────────────────────────
     VOICE RECORDING FUNCTIONALITY
     ───────────────────────────────────────────────── */
  const voiceBtn = document.getElementById('voiceBtn');
  const chatInput = document.getElementById('chatInput');
  
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
     CHAT INPUT HANDLING & Q&A RESPONSES
     ───────────────────────────────────────────────── */
  const sendChatBtn = document.getElementById('sendChatBtn');
  
  if (sendChatBtn && chatInput) {
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

      // Get AI response based on context
      setTimeout(() => {
        const response = getSimulationChatResponse(message);
        addChatMessage('assistant', response);
      }, 600);
    }

    sendChatBtn.addEventListener('click', handleSendChat);

    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendChat();
      }
    });
  }

  // Intelligent Q&A response system for Simulation page
  function getSimulationChatResponse(question) {
    const q = question.toLowerCase();
    
    // Check current page/step
    const isUploadPage = document.getElementById('pageUpload')?.classList.contains('active');
    const isTargetsPage = document.getElementById('pageTargets')?.classList.contains('active');
    const isSimPage = document.getElementById('pageSim')?.classList.contains('active');
    
    // Questions about what to do
    if (q.includes('what') && (q.includes('need to do') || q.includes('should i do') || q.includes('do i need') || q.includes('i need to do') || q.includes('to do'))) {
      if (isUploadPage) {
        return `📂 <b>You need to upload CSV files.</b><br><br>
          Here's what to do:<br>
          1. Click on the <b>drop zone</b> or drag and drop your CSV files<br>
          2. Upload all the hospital operational data files (around 50 CSV files expected)<br>
          3. Optionally, upload a <b>cost master file</b> for accurate cost calculations<br>
          4. Once files are loaded, click <b>"Process & Continue"</b> to proceed<br><br>
          The system will automatically detect file types and fit formula coefficients for the simulation.`;
      } else if (isTargetsPage) {
        return `🎯 <b>Select your target KPIs.</b><br><br>
          On this page, you need to:<br>
          1. Choose the Key Performance Indicators (KPIs) you want to improve<br>
          2. Set target values for each selected KPI<br>
          3. The system will identify which parameters can be adjusted to achieve these targets<br><br>
          Click on a KPI card to select/deselect it, then proceed to simulation.`;
      } else if (isSimPage) {
        return `⚙️ <b>Run the simulation.</b><br><br>
          On this page, you can:<br>
          1. Adjust the recommended parameters using the sliders<br>
          2. See real-time impact on your selected KPIs<br>
          3. Review the projected outcomes<br>
          4. Approve changes and generate an implementation plan<br><br>
          The simulation engine shows you how parameter changes affect your targets.`;
      }
      return `I'm here to help! Please tell me more about what you're trying to accomplish, and I'll guide you through the process.`;
    }
    
    // Questions about CSV files
    if (q.includes('csv') || q.includes('file') || q.includes('upload') || q.includes('data')) {
      return `📁 <b>About CSV Files:</b><br><br>
        The simulation engine requires hospital operational data in CSV format. This typically includes:<br>
        • Daily revenue and admission data<br>
        • Department-wise performance metrics<br>
        • Resource utilization data<br>
        • Cost and expense records<br><br>
        Simply drag and drop all your CSV files into the upload zone, or click to browse. The system will automatically identify and process each file type.`;
    }
    
    // Questions about simulation
    if (q.includes('simulation') || q.includes('simulate') || q.includes('how does') || q.includes('how it work')) {
      return `🔬 <b>About the Simulation Engine:</b><br><br>
        The Virevo Simulation Engine:<br>
        1. <b>Analyzes</b> your hospital's operational data<br>
        2. <b>Identifies</b> key parameters that influence your KPIs<br>
        3. <b>Simulates</b> the impact of changes before implementation<br>
        4. <b>Recommends</b> optimal parameter adjustments<br>
        5. <b>Generates</b> an actionable implementation plan<br><br>
        This allows you to test scenarios and predict outcomes without real-world risk.`;
    }
    
    // Help or guidance
    if (q.includes('help') || q.includes('guide') || q.includes('assist') || q.includes('stuck')) {
      return `🤝 <b>I'm here to help!</b><br><br>
        You can ask me:<br>
        • "What do I need to do?" - Get step-by-step guidance<br>
        • "How does the simulation work?" - Learn about the process<br>
        • "What files do I need?" - Understand data requirements<br>
        • "What are KPIs?" - Learn about performance indicators<br><br>
        Feel free to ask any question about the simulation process!`;
    }
    
    // KPI related questions
    if (q.includes('kpi') || q.includes('target') || q.includes('metric') || q.includes('indicator')) {
      return `📊 <b>About KPIs (Key Performance Indicators):</b><br><br>
        KPIs are measurable values that demonstrate how effectively the hospital is achieving key objectives. Examples include:<br>
        • <b>EBITDA %</b> - Profitability measure<br>
        • <b>Bed Occupancy</b> - Utilization efficiency<br>
        • <b>Length of Stay</b> - Patient flow metric<br>
        • <b>Drug Cost %</b> - Cost control indicator<br><br>
        Select the KPIs most important to your goals, and the simulation will show how to improve them.`;
    }
    
    // Default response
    return `Thanks for your question! I'm the Virevo AI assistant for the Simulation Engine.<br><br>
      Currently, you're on the <b>Upload Data</b> step. To proceed:<br>
      1. Upload your hospital's CSV data files<br>
      2. The system will process and analyze the data<br>
      3. You'll then select target KPIs and run simulations<br><br>
      Ask me "What do I need to do?" for detailed guidance at any step!`;
  }

});
