/* ═══════════════════════════════════════════════════
   Virevo App — Main JavaScript
   ═══════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

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
     SESSION MANAGEMENT
     ───────────────────────────────────────────────── */
  function saveSession(email, name) {
    const session = {
      email: email,
      name: name,
      loggedIn: true,
      timestamp: Date.now()
    };
    sessionStorage.setItem('virevo-session', JSON.stringify(session));
  }

  function getSession() {
    const session = sessionStorage.getItem('virevo-session');
    return session ? JSON.parse(session) : null;
  }

  function clearSession() {
    sessionStorage.removeItem('virevo-session');
    sessionStorage.removeItem('virevo-query');
    sessionStorage.removeItem('virevo-attachments');
  }

  // Check for existing session
  const existingSession = getSession();
  const loginScene = document.getElementById('loginScene');
  const appShell = document.getElementById('appShell');

  if (existingSession && existingSession.loggedIn && loginScene && appShell) {
    // User is already logged in, show app directly
    loginScene.style.display = 'none';
    const firstName = existingSession.name.split(' ')[0];
    const homeUserName = document.getElementById('homeUserName');
    const dashGreetName = document.getElementById('dashGreetName');
    if (homeUserName) homeUserName.textContent = firstName;
    if (dashGreetName) dashGreetName.textContent = firstName;
    appShell.classList.add('active');
  }


  /* ─────────────────────────────────────────────────
     STATE
     ───────────────────────────────────────────────── */
  let userEmail = existingSession ? existingSession.email : '';
  let userName = existingSession ? existingSession.name : '';


  /* ─────────────────────────────────────────────────
     DOM REFERENCES
     ───────────────────────────────────────────────── */
  const stepEmail     = document.getElementById('stepEmail');
  const stepPassword  = document.getElementById('stepPassword');
  const emailInput    = document.getElementById('emailInput');
  const passwordInput = document.getElementById('passwordInput');
  const emailError    = document.getElementById('emailError');
  const passError     = document.getElementById('passError');
  const btnEmailNext  = document.getElementById('btnEmailNext');
  const btnLogin      = document.getElementById('btnLogin');


  /* ─────────────────────────────────────────────────
     UTILITY FUNCTIONS
     ───────────────────────────────────────────────── */
  function showStep(step) {
    document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
    step.classList.add('active');
  }

  function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function extractName(email) {
    const local = email.split('@')[0];
    return local
      .replace(/[._-]/g, ' ')
      .replace(/\b\w/g, c => c.toUpperCase());
  }

  function getInitials(name) {
    return name
      .split(' ')
      .map(w => w[0])
      .join('')
      .substring(0, 2)
      .toUpperCase();
  }


  /* ─────────────────────────────────────────────────
     STEP 1 — EMAIL
     ───────────────────────────────────────────────── */
  if (btnEmailNext) {
    btnEmailNext.addEventListener('click', () => {
      const email = emailInput.value.trim();

      if (!validateEmail(email)) {
        emailError.classList.add('show');
        emailInput.focus();
        return;
      }

      emailError.classList.remove('show');
      userEmail = email;
      userName = extractName(email);

      btnEmailNext.classList.add('loading');

      setTimeout(() => {
        btnEmailNext.classList.remove('loading');
        document.getElementById('emailTextDisplay').textContent = userEmail;
        document.getElementById('emailAvatar').textContent = getInitials(userName);
        showStep(stepPassword);
        passwordInput.focus();
      }, 800);
    });
  }

  if (emailInput) {
    emailInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') btnEmailNext.click();
      emailError.classList.remove('show');
    });
  }

  // Change email button
  const changeEmailBtn = document.getElementById('changeEmail');
  if (changeEmailBtn) {
    changeEmailBtn.addEventListener('click', () => {
      showStep(stepEmail);
      emailInput.focus();
    });
  }

  // Toggle password visibility
  const togglePassBtn = document.getElementById('togglePass');
  if (togglePassBtn) {
    togglePassBtn.addEventListener('click', () => {
      passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
    });
  }


  /* ─────────────────────────────────────────────────
     STEP 2 — PASSWORD & LOGIN
     ───────────────────────────────────────────────── */
  if (btnLogin) {
    btnLogin.addEventListener('click', () => {
      if (passwordInput.value.length < 6) {
        passError.classList.add('show');
        passwordInput.focus();
        return;
      }

      passError.classList.remove('show');
      btnLogin.classList.add('loading');

      // Save session
      saveSession(userEmail, userName);

      setTimeout(() => {
        btnLogin.classList.remove('loading');
        launchApp();
      }, 1200);
    });
  }

  if (passwordInput) {
    passwordInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') btnLogin.click();
      passError.classList.remove('show');
    });
  }


  /* ─────────────────────────────────────────────────
     LAUNCH APP (Post-Login Transition)
     ───────────────────────────────────────────────── */
  function launchApp() {
    const loginScene = document.getElementById('loginScene');
    loginScene.classList.add('exit');

    setTimeout(() => {
      loginScene.style.display = 'none';

      const firstName = userName.split(' ')[0];
      document.getElementById('homeUserName').textContent = firstName;
      document.getElementById('dashGreetName').textContent = firstName;

      document.getElementById('appShell').classList.add('active');
    }, 600);
  }


  /* ─────────────────────────────────────────────────
     SIDEBAR TOGGLE
     ───────────────────────────────────────────────── */
  const sidebar = document.getElementById('appSidebar');
  const sidebarToggle = document.getElementById('sidebarToggle');

  if (sidebarToggle && sidebar && appShell) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      appShell.classList.toggle('sidebar-is-open');
    });
  }


  /* ─────────────────────────────────────────────────
     PAGE NAVIGATION (Home / Dashboard)
     ───────────────────────────────────────────────── */
  document.querySelectorAll('.nav-item[data-page]').forEach(item => {
    item.addEventListener('click', () => {
      // Update active nav
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      item.classList.add('active');

      // Switch pages
      document.getElementById('homePage').classList.remove('active');
      document.getElementById('dashPage').classList.remove('active');

      const targetId = item.dataset.page === 'home' ? 'homePage' : 'dashPage';
      document.getElementById(targetId).classList.add('active');
    });
  });


  /* ─────────────────────────────────────────────────
     THEME SWITCHER
     ───────────────────────────────────────────────── */
  const themeBtn     = document.getElementById('themeBtn');
  const themeDD      = document.getElementById('themeDropdown');
  const themeWrapper = document.getElementById('themeWrapper');

  // Load saved theme
  const savedTheme = localStorage.getItem('virevo-theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.querySelectorAll('.theme-option').forEach(o => {
      o.classList.toggle('active', o.dataset.theme === savedTheme);
    });
  }

  if (themeBtn && themeDD && themeWrapper) {
    // Toggle dropdown
    themeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      themeDD.classList.toggle('open');
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!themeWrapper.contains(e.target)) {
        themeDD.classList.remove('open');
      }
    });

    // Prevent dropdown from closing when clicking inside it
    themeDD.addEventListener('click', (e) => {
      e.stopPropagation();
    });

    // Theme option selection
    document.querySelectorAll('.theme-option').forEach(option => {
      option.addEventListener('click', () => {
        const theme = option.dataset.theme;

        // Apply theme
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('virevo-theme', theme);

        // Toggle active states (radio-button behavior)
        document.querySelectorAll('.theme-option').forEach(o => o.classList.remove('active'));
        option.classList.add('active');

        // Close dropdown after brief delay
        setTimeout(() => themeDD.classList.remove('open'), 350);
      });
    });
  }


  /* ─────────────────────────────────────────────────
     TEXTAREA AUTO-RESIZE
     ───────────────────────────────────────────────── */
  const chatTextarea = document.getElementById('chatTextarea');

  chatTextarea.addEventListener('input', () => {
    chatTextarea.style.height = 'auto';
    chatTextarea.style.height = Math.min(chatTextarea.scrollHeight, 160) + 'px';
  });


  /* ─────────────────────────────────────────────────
     FILE ATTACHMENT FUNCTIONALITY
     ───────────────────────────────────────────────── */
  const fileInput = document.getElementById('fileInput');
  const attachBtn = document.getElementById('attachBtn');
  const attachmentPreview = document.getElementById('attachmentPreview');
  const sendBtn = document.getElementById('sendBtn');
  let attachedFiles = [];

  // Trigger file input when attach button is clicked
  if (attachBtn && fileInput) {
    attachBtn.addEventListener('click', () => {
      fileInput.click();
    });

    // Handle file selection
    fileInput.addEventListener('change', (e) => {
      const files = Array.from(e.target.files);
      
      files.forEach(file => {
        // Validate file type
        const validTypes = ['application/pdf', 'application/msword', 
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                           'image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        
        if (!validTypes.includes(file.type) && !file.type.startsWith('image/')) {
          alert('Please upload PDF, DOC, or image files only.');
          return;
        }

        // Check file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
          alert('File size should be less than 10MB.');
          return;
        }

        attachedFiles.push(file);
        renderAttachmentPreview();
      });

      // Reset file input
      fileInput.value = '';
    });
  }

  function renderAttachmentPreview() {
    if (!attachmentPreview) return;
    
    attachmentPreview.innerHTML = '';
    
    if (attachedFiles.length === 0) {
      attachmentPreview.classList.remove('has-files');
      return;
    }

    attachmentPreview.classList.add('has-files');

    attachedFiles.forEach((file, index) => {
      const item = document.createElement('div');
      item.className = 'attachment-item';

      // Determine file type for icon
      let iconClass = 'image';
      let iconSvg = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>`;
      
      if (file.type === 'application/pdf') {
        iconClass = 'pdf';
        iconSvg = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M9 15h6"/></svg>`;
      } else if (file.type.includes('word') || file.type === 'application/msword') {
        iconClass = 'doc';
        iconSvg = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>`;
      }

      // Create image thumbnail for image files
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const img = item.querySelector('.image-thumb');
          if (img) img.src = e.target.result;
        };
        reader.readAsDataURL(file);
        
        item.innerHTML = `
          <img class="image-thumb" src="" alt="${file.name}">
          <span class="file-name">${file.name}</span>
          <button class="remove-file" data-index="${index}" title="Remove">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        `;
      } else {
        item.innerHTML = `
          <div class="file-icon ${iconClass}">${iconSvg}</div>
          <span class="file-name">${file.name}</span>
          <button class="remove-file" data-index="${index}" title="Remove">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        `;
      }

      attachmentPreview.appendChild(item);
    });

    // Add remove button listeners
    attachmentPreview.querySelectorAll('.remove-file').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const index = parseInt(btn.dataset.index);
        attachedFiles.splice(index, 1);
        renderAttachmentPreview();
      });
    });
  }


  /* ─────────────────────────────────────────────────
     TOJO CONVERSATION ENGINE
     Based on Conversation_Script.md
     ───────────────────────────────────────────────── */
  const tojoConversation = {
    state: 'INITIAL',
    step1: {
      coveredTopics: new Set(),
      firedProbes: new Set(),
      activeProbe: null,
      mriStage: null
    },
    
    // Topic detection for hospital details
    topics: {
      beds: {
        patterns: [/150 beds?/i, /\b12 icu\b/i, /\b6 nicu\b/i, /\b3 ot/i, /operating theatres?/i, /\bicu beds?\b/i, /\bnicu\b/i, /(general|semi-private|private) (beds?|ward)/i, /\d+ beds?/i],
        ack: '– Bed capacity and configuration noted'
      },
      specialties: {
        patterns: [/ortho/i, /gen(eral)? surg/i, /gyn(a|ae)/i, /internal med/i, /cardio/i, /visiting/i, /multispecialty/i, /specialt/i],
        ack: '– Specialties noted'
      },
      location: {
        patterns: [/nashik/i, /maharashtra/i, /tier[- ]?2/i, /city/i, /location/i],
        ack: '– Location noted'
      },
      revenue_stagnation: {
        patterns: [/revenue.{0,30}(flat|stagnant|stuck|not grow|not improving)/i, /\d+ ?cr/i, /crore/i, /high occupan|occupan.{0,20}high/i, /\d+% ?occupan/i],
        ack: '– Revenue and occupancy data noted'
      },
      ebitda: {
        patterns: [/ebitda/i, /\d+ ?%/i, /everything (looks|seems) (equally )?important/i, /don'?t know (where|which) to focus/i, /which (lever|area|aspect) to (pull|focus|prioritise|prioritize)/i, /profit/i, /margin/i],
        ack: '– Financial metrics and priorities noted'
      },
      los: {
        patterns: [/\blos\b/i, /length of stay/i, /(\d+|five|four|three) days?/i, /(higher|longer) than (benchmark|target|expected)/i, /staying (too )?long/i],
        ack: '– Length of stay concerns noted'
      },
      diagnostic_leakage: {
        patterns: [/diagnostic leakage/i, /leak(age|ing)/i, /scans? going (out|outside)/i, /outside scans?/i, /mri/i, /ct scan/i],
        ack: '– Diagnostic leakage flagged'
      },
      marketing: {
        patterns: [/marketing/i, /footfall/i, /opd.{0,20}(full|maxed|capacity)/i, /more patients/i, /grow (the )?opd/i],
        ack: '– Marketing and OPD capacity noted'
      },
      manpower: {
        patterns: [/manpower/i, /staff(ing| costs?)/i, /agency nurs/i, /nurs(e|ing) costs?/i, /rationali[sz]e/i, /efficiency/i, /(cut|reduce|trim) (staff|nursing|costs?)/i],
        ack: '– Manpower and staffing concerns noted'
      }
    },
    
    // Probes to ask in sequence
    probes: [
      {
        id: 'mri',
        question: `Before you go further — **how many MRI units do you have, and are they in-house or outsourced?**\n\n*(Diagnostic capacity is one of the quietest LOS levers — worth pinning early.)*`,
        stage_one_triggers: [/\b1 mri\b/i, /one mri/i, /single mri/i, /mri.{0,15}outsourced/i, /outsourced.{0,15}mri/i, /vendor/i, /in-?house/i, /\d+ mri/i],
        stage_one_followup: `Noted. Worth flagging: diagnostic leakage in most units isn't about referrals going elsewhere — it's about **slot availability**. Patients who can't get a scan in 4 hours get sent out, and the case clock keeps running. Have you ever evaluated adding MRI capacity?`,
        stage_two_triggers: [/capex/i, /\bcost\b/i, /steep/i, /expensive/i, /not (sure|convinced)/i, /volumes?/i, /justify/i, /(roi|return)/i, /maybe (later|down the line)/i, /not (now|yet)/i, /yes/i, /no/i, /consider/i],
        stage_two_response: `Fair concern. Parking it as an option, not a recommendation. The Agent will pull leakage volumes and run a capex-vs-return simulation before we revisit. Carry on with anything else on your mind.`
      },
      {
        id: 'icu_protocol',
        question: `On operations — **who sets the ICU admission and step-down protocols? And what's your nurse-to-bed ratio in ICU right now?**\n\n*(ICU LOS and delayed step-downs usually drive overall LOS more than ward stays.)*`,
        response_triggers: [/intensivist/i, /protocol/i, /judg(e)?ment/i, /\b1:\d\b/i, /\d to \d/i, /\bratio\b/i, /hospitalist/i, /doctor/i, /nurse/i],
        followup: `Noted. We'll cross-check protocol adherence against actual ICU LOS once data is in.`
      },
      {
        id: 'rounds',
        question: `One more — **what time do your consultants do morning in-patient rounds? And are they generally open to routine changes if data showed it was worth it?**\n\n*(Round timing sets the discharge clock for the whole day. Often invisible.)*`,
        response_triggers: [/\d+:\d+/i, /\d+ ?am/i, /\d+ ?o'?clock/i, /morning/i, /rounds?/i, /open/i, /not (open|all)/i, /mix(ed)?/i, /some are/i],
        followup: `Noted. All of this becomes clearer once the **Virevo CEO Agent** and I work through the datasets. I'll come back with numbers, not opinions.\n\nAnything else on your mind, or shall I summarize what I have?`
      }
    ],
    
    // Trigger patterns for different states
    triggers: {
      opening: [/how (do|should) (i|we) (start|begin|proceed|do this)/i, /where do (i|we) (start|begin)/i, /what (do|should) i do (now|first|next)/i, /how does this work/i, /ready to start/i, /^\s*(start|begin|hi|hello|hey)\s*$/i, /get started/i],
      stepByStep: [/step by step/i, /one (step )?at a time/i, /one by one/i, /as we go/i, /walk me through/i, /take me through/i, /each step/i, /the (latter|second)/i],
      endToEnd: [/end.{0,5}to.{0,5}end/i, /whole process/i, /overview/i, /the (former|first)/i, /all at once/i],
      wrap: [/that.{0,15}(covers|is it|are the main)/i, /you have enough/i, /enough to start/i, /^that'?s (it|all)/i, /^no(thing)? (else|more)/i, /read.{0,5}back/i, /summary/i, /summari[sz]e/i],
      consent: [/^\s*(yes|sure|ok(ay)?|go ahead|continue|next|proceed)/i, /step ?2/i, /move on/i, /let'?s (continue|go|move|proceed)/i],
      acknowledgment: [/^\s*(ok(ay)?|sure|sounds good|acknowledg|got it|alright|will wait|fine|noted|thanks?|thank you)/i]
    },
    
    // Responses for each state
    responses: {
      intro: `Hi! I'm **Tojo** — your point of contact through this engagement. Working with me is the **Virevo CEO Agent**: the analytical engine that ingests your hospital's data, builds a mathematical model of how everything fits together, and runs the simulations we'll use to make decisions. I handle the conversation; the Agent handles the maths.\n\nQuick choice before we begin: do you want me to walk you through the **whole process end-to-end** first, or take it **one step at a time** and explain each step as we get there?`,
      
      step1Intro: `Good. We'll start with **Step 1 — Project Brief and Problem Statement.**\n\nThis part is a conversation. I need to understand your hospital — what it does, how it runs, what's working, what isn't. You can **type or use voice**.\n\nShare whatever feels relevant — size, specialties, the problems on your mind, the causes you've already identified, anything you think I should know. I'll interject only when I need a clarification.\n\nTake your time. Go ahead.`,
      
      endToEndOverview: `Here's the full process:\n\n**Step 1 — Project Brief:** A conversation where I understand your hospital and its challenges.\n\n**Step 2 — Data Monitoring:** The Agent ingests 12-18 months of historical data, then monitors live operations for 4-8 weeks.\n\n**Step 3 — Analysis:** We identify root causes and build simulations.\n\n**Step 4 — Recommendations:** Prioritized interventions with projected impact.\n\n**Step 5 — Implementation:** Tracked execution with the dashboard.\n\nReady to start with Step 1?`,
      
      step1Summary: `Right. Let me read back what I have so we're aligned.\n\n**What I've logged:**\n{TOPICS}\n\n**Items flagged for deeper analysis:**\n{PROBES}\n\nEnough to start. I'll compile the **data access request** — what we need from your HIS, billing, HR, pharmacy, and maintenance logs. You'll sign off the read permissions and we begin.\n\nReady for **Step 2**?`,
      
      step2Intro: `**Step 2 — Model Validation and Data Monitoring.**\n\nTwo streams running in parallel:\n\n**1. Retrospective build.** The Agent ingests the last 12-18 months of operational data. This becomes the historical baseline. Roughly 4-6 weeks.\n\n**2. Live monitoring.** Once retrospective is loaded, the Agent tracks live data for 4-8 weeks to validate the model.\n\nI won't go silent. You'll get periodic updates — coverage levels, early signals, anomalies worth flagging.\n\nOnce you authorise the data access request, the Agent starts. First update in about two weeks.`,
      
      week2Update: `**Update — Week 2 of Step 2**\n\nStatus:\n– **HIS:** connected, retrospective ingestion at ~68% coverage. On track.\n– **Billing:** connected, ~52% coverage. Some line-item gaps — Agent is reconciling.\n– **HR system:** connected, full coverage.\n– **Accounts:** GL bridge built, monthly pulls running clean.\n– **Pharmacy:** records sparse pre-October. Agent rebuilding from dispensing logs.\n\nEarly signal worth flagging: **OT cancellation rate looks meaningfully above benchmark.** Investigating. More in the next update.`,
      
      week5Update: `**Update — Week 5 of Step 2**\n\nRetrospective build effectively complete. Live monitoring running with three weeks of clean overlap.\n\nThree preliminary observations:\n\n1. **OT cancellations cluster on specific weekdays.** Pattern too clean to be random. Correlating against equipment maintenance.\n\n2. **ICU LOS materially above benchmark.** Non-trivial share of patients clinically ready for step-down 12-36 hours earlier.\n\n3. **Insurance receivables ageing heavier than expected.** Separating submission lag from query-response lag.\n\nNone of these are conclusions yet. That's the **Step 3** conversation.`,
      
      fallback: `I didn't quite catch that. Could you rephrase? Or tell me more about your hospital's operations and challenges.`
    },
    
    processMessage(text) {
      const t = text.toLowerCase();
      
      // Initial state - waiting for opening
      if (this.state === 'INITIAL') {
        if (this.triggers.opening.some(p => p.test(text))) {
          this.state = 'INTRO_GIVEN';
          return this.responses.intro;
        }
        // Any input triggers intro
        this.state = 'INTRO_GIVEN';
        return this.responses.intro;
      }
      
      // After intro - waiting for step-by-step or end-to-end choice
      if (this.state === 'INTRO_GIVEN') {
        if (this.triggers.stepByStep.some(p => p.test(text))) {
          this.state = 'STEP1_LISTENER';
          return this.responses.step1Intro;
        }
        if (this.triggers.endToEnd.some(p => p.test(text))) {
          this.state = 'OVERVIEW_GIVEN';
          return this.responses.endToEndOverview;
        }
        // Default to step by step
        this.state = 'STEP1_LISTENER';
        return this.responses.step1Intro;
      }
      
      // After overview - ready to start step 1
      if (this.state === 'OVERVIEW_GIVEN') {
        if (this.triggers.consent.some(p => p.test(text))) {
          this.state = 'STEP1_LISTENER';
          return this.responses.step1Intro;
        }
        this.state = 'STEP1_LISTENER';
        return this.responses.step1Intro;
      }
      
      // Step 1 listener - multi-topic detection
      if (this.state === 'STEP1_LISTENER') {
        return this.handleStep1(text);
      }
      
      // Step 1 summary given - waiting for consent to Step 2
      if (this.state === 'STEP1_DONE') {
        if (this.triggers.consent.some(p => p.test(text))) {
          this.state = 'STEP2_INTRO';
          return this.responses.step2Intro;
        }
        return `Ready for **Step 2**? Say yes to continue.`;
      }
      
      // Step 2 intro given - waiting for acknowledgment
      if (this.state === 'STEP2_INTRO') {
        if (this.triggers.acknowledgment.some(p => p.test(text))) {
          this.state = 'STEP2_WEEK2';
          return this.responses.week2Update;
        }
        return this.responses.step2Intro;
      }
      
      // Week 2 update - waiting for acknowledgment
      if (this.state === 'STEP2_WEEK2') {
        if (this.triggers.acknowledgment.some(p => p.test(text))) {
          this.state = 'STEP2_WEEK5';
          return this.responses.week5Update;
        }
        return `Noted. The Agent continues processing. Any questions about the Week 2 status?`;
      }
      
      // Week 5 update - end of current script
      if (this.state === 'STEP2_WEEK5') {
        return `The model validation is progressing well. Step 3 — the detailed analysis and root cause identification — will begin once live monitoring completes. Any questions about what we've observed so far?`;
      }
      
      return this.responses.fallback;
    },
    
    handleStep1(text) {
      // Check for wrap signal
      if (this.triggers.wrap.some(p => p.test(text))) {
        return this.generateSummary();
      }
      
      // If we're in a probe, handle that first
      if (this.step1.activeProbe) {
        return this.resolveProbe(text);
      }
      
      // Detect topics in the message
      const matched = [];
      for (const [key, topic] of Object.entries(this.topics)) {
        if (this.step1.coveredTopics.has(key)) continue;
        if (topic.patterns.some(p => p.test(text))) {
          matched.push({ key, ...topic });
          this.step1.coveredTopics.add(key);
        }
      }
      
      let response = '';
      
      // Acknowledge detected topics
      if (matched.length > 0) {
        response = `**Logged:**\n${matched.map(t => t.ack).join('\n')}`;
      }
      
      // Fire next unfired probe
      const nextProbe = this.probes.find(p => !this.step1.firedProbes.has(p.id));
      if (nextProbe) {
        this.step1.firedProbes.add(nextProbe.id);
        this.step1.activeProbe = nextProbe.id;
        response += (response ? '\n\n' : '') + nextProbe.question;
      } else if (matched.length > 0) {
        response += `\n\nAnything else, or shall I read back what I have?`;
      } else if (this.step1.coveredTopics.size > 0) {
        response = `Go on — I'm listening. Or say "that's it" when you're done.`;
      } else {
        response = `Tell me about your hospital — size, specialties, location, the problems you're facing, anything you think is relevant. I'll ask clarifying questions as needed.`;
      }
      
      return response;
    },
    
    resolveProbe(text) {
      const probe = this.probes.find(p => p.id === this.step1.activeProbe);
      
      // MRI probe is 2-stage
      if (probe.id === 'mri') {
        if (this.step1.mriStage === null || this.step1.mriStage === 'asked') {
          if (probe.stage_one_triggers.some(p => p.test(text))) {
            this.step1.mriStage = 'followup';
            return probe.stage_one_followup;
          }
        }
        if (this.step1.mriStage === 'followup') {
          if (probe.stage_two_triggers.some(p => p.test(text))) {
            this.step1.mriStage = 'done';
            this.step1.activeProbe = null;
            return probe.stage_two_response;
          }
        }
        // Default: accept any response and move on
        this.step1.mriStage = 'done';
        this.step1.activeProbe = null;
        return probe.stage_two_response;
      }
      
      // Single-stage probes
      if (probe.response_triggers && probe.response_triggers.some(p => p.test(text))) {
        this.step1.activeProbe = null;
        return probe.followup;
      }
      
      // Accept any response
      this.step1.activeProbe = null;
      return probe.followup;
    },
    
    generateSummary() {
      this.state = 'STEP1_DONE';
      
      const topicsList = Array.from(this.step1.coveredTopics).map(key => {
        const topic = this.topics[key];
        return topic ? topic.ack : `– ${key}`;
      }).join('\n');
      
      const probesList = Array.from(this.step1.firedProbes).map(id => {
        const probe = this.probes.find(p => p.id === id);
        return probe ? `– ${probe.id.replace('_', ' ').toUpperCase()}: flagged for analysis` : '';
      }).filter(Boolean).join('\n');
      
      return this.responses.step1Summary
        .replace('{TOPICS}', topicsList || '– No specific topics logged yet')
        .replace('{PROBES}', probesList || '– Standard analysis scope');
    }
  };


  /* ─────────────────────────────────────────────────
     CHAT MESSAGES DISPLAY
     ───────────────────────────────────────────────── */
  const chatMessagesArea = document.getElementById('chatMessagesArea');
  
  function addChatMessage(type, content) {
    if (!chatMessagesArea) return;
    
    const msg = document.createElement('div');
    msg.className = `chat-message ${type}`;
    msg.innerHTML = `
      <div class="msg-content">${content.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>')}</div>
      <div class="msg-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
    `;
    chatMessagesArea.appendChild(msg);
    chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight;
    
    // Show messages area
    chatMessagesArea.classList.add('has-messages');
  }
  
  function showTypingIndicator() {
    if (!chatMessagesArea) return null;
    
    const typing = document.createElement('div');
    typing.className = 'chat-message assistant typing';
    typing.innerHTML = `
      <div class="typing-indicator">
        <span></span><span></span><span></span>
      </div>
    `;
    chatMessagesArea.appendChild(typing);
    chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight;
    return typing;
  }


  /* ─────────────────────────────────────────────────
     SEND MESSAGE FUNCTIONALITY
     ───────────────────────────────────────────────── */
  if (sendBtn && chatTextarea) {
    sendBtn.addEventListener('click', sendMessage);
    
    chatTextarea.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
  }

  function sendMessage() {
    const message = chatTextarea.value.trim();
    
    if (!message && attachedFiles.length === 0) {
      return;
    }

    // Check for upload-related queries - redirect to simulation.html
    const uploadPatterns = [
      /where (do|can|should) (i|we) upload/i,
      /how (do|can|should) (i|we) upload/i,
      /upload (files?|data|csv)/i,
      /where.*upload/i,
      /upload.*where/i,
      /start upload/i,
      /begin upload/i,
      /ready to upload/i,
      /let'?s upload/i,
      /want to upload/i,
      /need to upload/i,
      /show.*upload/i,
      /take me to upload/i,
      /go to upload/i
    ];
    
    const isUploadQuery = uploadPatterns.some(p => p.test(message));
    
    if (isUploadQuery) {
      // Add user message to chat
      addChatMessage('user', message);
      
      // Clear input
      chatTextarea.value = '';
      chatTextarea.style.height = 'auto';
      
      // Show typing indicator
      const typingIndicator = showTypingIndicator();
      
      // Save conversation state for simulation.html to continue
      sessionStorage.setItem('virevo-conversation-state', JSON.stringify({
        state: tojoConversation.state,
        step1: {
          coveredTopics: Array.from(tojoConversation.step1.coveredTopics),
          firedProbes: Array.from(tojoConversation.step1.firedProbes),
          activeProbe: tojoConversation.step1.activeProbe,
          mriStage: tojoConversation.step1.mriStage
        }
      }));
      sessionStorage.setItem('virevo-upload-redirect', 'true');
      sessionStorage.setItem('virevo-user-query', message);
      
      // Show response and redirect
      setTimeout(() => {
        if (typingIndicator) typingIndicator.remove();
        addChatMessage('assistant', `Perfect! I'll take you to the **Upload section** now. This is where you'll upload your hospital's CSV data files — billing records, patient data, HR information, and operational logs.\n\nRedirecting...`);
        
        // Redirect after a brief moment
        setTimeout(() => {
          window.location.href = 'simulation.html';
        }, 1500);
      }, 800);
      
      return;
    }

    // Add user message to chat
    let userContent = message;
    if (attachedFiles.length > 0) {
      userContent += `<br><small style="opacity: 0.7;">📎 ${attachedFiles.map(f => f.name).join(', ')}</small>`;
    }
    addChatMessage('user', userContent);
    
    // Clear input
    chatTextarea.value = '';
    chatTextarea.style.height = 'auto';
    attachedFiles = [];
    renderAttachmentPreview();
    
    // Show typing indicator
    const typingIndicator = showTypingIndicator();
    
    // Get AI response after a short delay
    setTimeout(() => {
      if (typingIndicator) typingIndicator.remove();
      
      const response = tojoConversation.processMessage(message);
      addChatMessage('assistant', response);
    }, 800 + Math.random() * 700);
  }


  /* ─────────────────────────────────────────────────
     VOICE RECORDING FUNCTIONALITY
     ───────────────────────────────────────────────── */
  const voiceBtn = document.getElementById('voiceBtn');
  
  if (voiceBtn && chatTextarea) {
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
          previousText = chatTextarea.value;
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
        chatTextarea.value = previousText + separator + (finalTranscript || interimTranscript);
        
        // Trigger input event for auto-resize
        chatTextarea.dispatchEvent(new Event('input'));
        
        // Update previousText when we get final results
        if (finalTranscript) {
          previousText = chatTextarea.value;
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

});
