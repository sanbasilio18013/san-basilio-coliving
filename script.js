/**
 * San Basilio Premium Coliving - Script de Funcionalidades
 * Vanilla JavaScript para interacciones rápidas y fluidas.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Inicializar los Iconos Lucide (por si se usan iconos adicionales)
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  // 2. Efecto dinámico en el Header (Menú superior) al hacer Scroll
  const header = document.querySelector('header');
  const handleScroll = () => {
    if (window.scrollY > 20) {
      header.classList.add('header-scrolled');
    } else {
      header.classList.remove('header-scrolled');
    }
  };
  
  // Ejecutar al inicio y en cada evento de scroll
  window.addEventListener('scroll', handleScroll);
  handleScroll();

  // 3. Menú Móvil (Drawer)
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      mobileMenu.classList.toggle('hidden');
      
      // Rotar ligeramente el botón de menú para feedback visual
      mobileMenuBtn.classList.toggle('rotate-90');
    });

    // Cerrar menú móvil al hacer clic en un enlace
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
        mobileMenuBtn.classList.remove('rotate-90');
      });
    });

    // Cerrar menú móvil al hacer clic fuera del mismo
    document.addEventListener('click', (e) => {
      if (!mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
        mobileMenu.classList.add('hidden');
        mobileMenuBtn.classList.remove('rotate-90');
      }
    });
  }

  // 4. Gestión de Carruseles de Habitaciones y Zonas Comunes (Dinámico y Táctil)
  const carousels = document.querySelectorAll('[data-carousel]');

  carousels.forEach(carousel => {
    const track = carousel.querySelector('.carousel-track');
    const slides = carousel.querySelectorAll('.carousel-slide');
    const prevBtn = carousel.querySelector('.carousel-prev');
    const nextBtn = carousel.querySelector('.carousel-next');
    const dots = carousel.querySelectorAll('.carousel-dots button');
    
    let currentIndex = 0;
    const totalSlides = slides.length;

    // Función para actualizar la posición del carrusel
    const updateCarousel = () => {
      if (track) {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
      }
      
      // Sincronizar dots
      dots.forEach((dot, index) => {
        if (index === currentIndex) {
          dot.classList.remove('bg-white/50');
          dot.classList.add('bg-[#5f6f5e]', 'w-5'); // Se cambia a color olive del tema para mejor visibilidad
        } else {
          dot.classList.remove('bg-[#5f6f5e]', 'w-5');
          dot.classList.add('bg-white/50');
        }
      });
    };

    // Botón Siguiente
    const showNext = () => {
      currentIndex = (currentIndex + 1) % totalSlides;
      updateCarousel();
    };

    // Botón Anterior
    const showPrev = () => {
      currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
      updateCarousel();
    };

    if (nextBtn) nextBtn.addEventListener('click', showNext);
    if (prevBtn) prevBtn.addEventListener('click', showPrev);

    // Click en Dots
    dots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        currentIndex = index;
        updateCarousel();
      });
    });

    // Soporte para deslizar en pantallas táctiles (Touch Gestures)
    let startX = 0;
    let endX = 0;

    carousel.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
    }, { passive: true });

    carousel.addEventListener('touchend', (e) => {
      endX = e.changedTouches[0].clientX;
      const diffX = startX - endX;
      
      // Deslizar con un mínimo de 50px de movimiento
      if (Math.abs(diffX) > 50) {
        if (diffX > 0) {
          showNext();
        } else {
          showPrev();
        }
      }
    }, { passive: true });

    // Inicializar estado visual del carrusel
    updateCarousel();
  });

  // 5. Preseleccionar Habitación desde las Tarjetas del Catálogo
  const selectRoomButtons = document.querySelectorAll('.select-room-btn');
  const roomSelect = document.getElementById('habitacion');
  
  selectRoomButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const roomValue = btn.getAttribute('data-room-value');
      
      if (roomSelect && roomValue) {
        roomSelect.value = roomValue;
        
        // Hacer scroll suave a la sección del formulario
        const targetSection = document.getElementById('solicitar');
        if (targetSection) {
          targetSection.scrollIntoView({ behavior: 'smooth' });
          
          // Dar un pequeño efecto visual de foco al dropdown de habitaciones
          setTimeout(() => {
            roomSelect.focus();
            roomSelect.classList.add('border-[#c76a53]', 'ring-3', 'ring-[#c76a53]/15');
            setTimeout(() => {
              roomSelect.classList.remove('border-[#c76a53]', 'ring-3', 'ring-[#c76a53]/15');
            }, 1200);
          }, 800);
        }
      }
    });
  });

  // 6. Scroll Suave para Enlaces de Navegación Locales
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });

  // 7. Modal Visor de Plano Interactivo
  const planoPreview = document.getElementById('plano-preview-container');
  const viewPlanoBtn = document.getElementById('view-plano-btn');
  const planoModal = document.getElementById('plano-modal');
  const closePlanoBtn = document.getElementById('close-plano-modal-btn');

  const showPlanoModal = () => {
    if (planoModal) {
      planoModal.classList.remove('hidden');
      document.body.classList.add('overflow-hidden');
    }
  };

  const hidePlanoModal = () => {
    if (planoModal) {
      planoModal.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
    }
  };

  if (planoPreview) planoPreview.addEventListener('click', showPlanoModal);
  if (viewPlanoBtn) viewPlanoBtn.addEventListener('click', showPlanoModal);
  if (closePlanoBtn) closePlanoBtn.addEventListener('click', hidePlanoModal);
  
  if (planoModal) {
    planoModal.addEventListener('click', (e) => {
      if (e.target === planoModal || e.target.classList.contains('bg-[#1d2320]/80')) {
        hidePlanoModal();
      }
    });
  }

  // 8. Envío de Formulario con AJAX / Fetch API a Google Apps Script
  const appForm = document.getElementById('application-form');
  const submitBtn = document.getElementById('submit-btn');
  const btnText = document.getElementById('btn-text');
  const btnSpinner = document.getElementById('btn-spinner');
  const formErrorBanner = document.getElementById('form-error-banner');
  const formErrorMsg = document.getElementById('form-error-msg');
  const successModal = document.getElementById('success-modal');
  const closeModalBtn = document.getElementById('close-modal-btn');

  // Control dinámico del campo "Año de curso" para Grado Universitario (Estilo inline robusto)
  const estudiosSelect = document.getElementById('estudios');
  const anoCursoContainer = document.getElementById('ano-curso-container');
  const anoCursoSelect = document.getElementById('ano_curso');

  if (estudiosSelect && anoCursoContainer && anoCursoSelect) {
    const toggleAnoCurso = () => {
      if (estudiosSelect.value === 'Grado Universitario') {
        anoCursoContainer.style.setProperty('display', 'flex', 'important');
        anoCursoSelect.required = true;
      } else {
        anoCursoContainer.style.setProperty('display', 'none', 'important');
        anoCursoSelect.required = false;
        anoCursoSelect.value = ''; // Limpiar selección
      }
    };

    // Ejecutar al cambiar y al cargar inicialmente
    estudiosSelect.addEventListener('change', toggleAnoCurso);
    toggleAnoCurso();
  }

  // URL del script de Google Apps (reemplazable por el cliente)
  const GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxnU042R1UHNdaZi-wE9KzJQuSxaV9Hgwd7bON3FM8E3I4_BjGyKvKjVELIlARMd00B/exec";

  if (appForm) {
    appForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      // Filtro Anti-Spam (Honeypot)
      const honeypot = document.getElementById('b_website') ? document.getElementById('b_website').value : '';
      if (honeypot) {
        console.warn("Spam detectado (Honeypot relleno).");
        // Simular éxito silencioso para desalentar al bot
        setLoadingState(true);
        setTimeout(() => {
          setLoadingState(false);
          showSuccessModal();
          appForm.reset();
        }, 1200);
        return;
      }
      
      // Ocultar banners de error previos
      formErrorBanner.classList.add('hidden');

      // Validaciones básicas extras
      const nombre = document.getElementById('nombre').value.trim();
      const telefono = document.getElementById('telefono').value.trim();
      const habitacion = document.getElementById('habitacion').value;
      const estudios = document.getElementById('estudios').value;
      const solvencia = document.getElementById('solvencia').value;
      const normas = document.getElementById('normas').checked;
      const privacidad = document.getElementById('privacidad').checked;
      const ano_curso = anoCursoSelect ? anoCursoSelect.value : '';

      if (!nombre || !telefono || !habitacion || !estudios || !solvencia || !normas || !privacidad) {
        showFormError("Por favor, rellene todos los campos obligatorios, acepte las normas de convivencia y la política de privacidad.");
        return;
      }

      if (estudios === 'Grado Universitario' && !ano_curso) {
        showFormError("Por favor, selecciona qué año de grado universitario estás cursando.");
        return;
      }

      // Activar estado de carga en el botón
      setLoadingState(true);

      // Recoger los datos del formulario
      const formData = new FormData(appForm);
      const dataObject = {};
      formData.forEach((value, key) => {
        dataObject[key] = value;
      });

      // Añadir marca de tiempo local
      dataObject['timestamp'] = new Date().toISOString();

      // Comprobar si la URL del script está configurada
      const isDemoMode = GOOGLE_SCRIPT_URL.includes("PEGA_AQUÍ_LA_URL");

      if (isDemoMode) {
        // Simular llamada de red exitosa para la demo
        console.warn("Modo Demo: No se ha configurado la URL real de Google Apps Script. Simulando envío...");
        setTimeout(() => {
          setLoadingState(false);
          showSuccessModal();
          appForm.reset();
        }, 1500);
      } else {
        try {
          // Realizar la petición Fetch a Google Apps Script
          const response = await fetch(GOOGLE_SCRIPT_URL, {
            method: 'POST',
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataObject)
          });

          // Procesar respuesta
          if (response.ok) {
            setLoadingState(false);
            showSuccessModal();
            appForm.reset();
          } else {
            throw new Error(`Error en el servidor: ${response.status}`);
          }
        } catch (error) {
          console.error("Error al enviar formulario:", error);
          
          try {
            console.log("Intentando envío alternativo sin CORS...");
            await fetch(GOOGLE_SCRIPT_URL, {
              method: 'POST',
              mode: 'no-cors',
              body: JSON.stringify(dataObject)
            });
            setLoadingState(false);
            showSuccessModal();
            appForm.reset();
          } catch (secondaryError) {
            setLoadingState(false);
            showFormError("Hubo un problema al enviar tu solicitud. Por favor, inténtalo de nuevo o contáctanos por WhatsApp directamente.");
          }
        }
      }
    });
  }

  // Funciones Auxiliares del Formulario
  function setLoadingState(isLoading) {
    if (submitBtn) {
      if (isLoading) {
        submitBtn.disabled = true;
        submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
        if (btnText) btnText.textContent = "Enviando solicitud...";
        if (btnSpinner) btnSpinner.classList.remove('hidden');
      } else {
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
        if (btnText) btnText.textContent = "Enviar Solicitud de Reserva";
        if (btnSpinner) btnSpinner.classList.add('hidden');
      }
    }
  }

  function showFormError(message) {
    if (formErrorMsg && formErrorBanner) {
      formErrorMsg.textContent = message;
      formErrorBanner.classList.remove('hidden');
      formErrorBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  function showSuccessModal() {
    if (successModal) {
      successModal.classList.remove('hidden');
      document.body.classList.add('overflow-hidden');
    }
  }

  function hideSuccessModal() {
    if (successModal) {
      successModal.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
    }
  }

  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', hideSuccessModal);
  }

  if (successModal) {
    successModal.addEventListener('click', (e) => {
      if (e.target === successModal || e.target.classList.contains('bg-[#1d2320]/40')) {
        hideSuccessModal();
      }
    });
  }
});
