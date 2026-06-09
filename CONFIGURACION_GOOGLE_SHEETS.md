# 📊 Configuración de Google Sheets para San Basilio Coliving

Esta guía te explica paso a paso cómo conectar el formulario de tu página web con una hoja de cálculo de Google Sheets de forma 100% gratuita y sin intermediarios.

---

## Paso 1: Crear la Hoja de Cálculo en Google Drive
1. Entra en tu cuenta de Google Drive y crea una nueva **Hoja de cálculo de Google** (Google Sheets).
2. Ponle un nombre identificativo, por ejemplo: `Registro Reservas - San Basilio Coliving`.
3. Deja la hoja en blanco (el script creará las cabeceras automáticamente con la primera solicitud).

---

## Paso 2: Configurar el Google Apps Script
1. En el menú superior de tu Hoja de cálculo, haz clic en **Extensiones** ➡️ **Apps Script**.
2. Se abrirá una pestaña nueva con un editor de código. Borra todo el código que aparezca por defecto en el archivo `Código.gs`.
3. Copia y pega exactamente el siguiente código de abajo:

```javascript
// CONFIGURACIÓN DE NOTIFICACIONES DE TELEGRAM (OPCIONAL)
// Si no deseas usar notificaciones, deja estas variables como están
var TELEGRAM_BOT_TOKEN = "PEGA_AQUÍ_EL_TOKEN_DEL_BOT"; // Ej: "123456789:ABCdef..."
var TELEGRAM_CHAT_ID = "PEGA_AQUÍ_EL_CHAT_ID";         // Ej: "987654321" o "-1001234567890"

function doPost(e) {
  try {
    // Obtener la hoja activa
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Parsear los datos recibidos
    var data = JSON.parse(e.postData.contents);
    
    // Crear cabeceras de columnas si la hoja está vacía
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "Fecha y Hora", 
        "Nombre y Apellidos", 
        "Teléfono (WhatsApp)", 
        "Correo Electrónico",
        "Habitación de Interés", 
        "Estudios / Profesión", 
        "Año de Curso", 
        "Meses de Alquiler",
        "Respaldo Financiero"
      ]);
      
      // Aplicar formato básico a la cabecera (Negrita y fondo gris claro)
      sheet.getRange("A1:I1").setFontWeight("bold").setBackground("#f3f3f3");
    }
    
    // Obtener la fecha y hora formateada en la zona horaria de España (Madrid)
    var fechaLocal = Utilities.formatDate(new Date(), "Europe/Madrid", "dd/MM/yyyy HH:mm:ss");
    
    // Insertar los datos del candidato en una nueva fila
    sheet.appendRow([
      fechaLocal,
      data.nombre || "",
      data.telefono || "",
      data.email || "",
      data.habitacion || "",
      data.estudios || "",
      data.ano_curso || "-",
      data.meses_alquiler || "",
      data.solvencia || ""
    ]);
    
    // Enviar notificación a Telegram si está configurado
    if (TELEGRAM_BOT_TOKEN && TELEGRAM_BOT_TOKEN !== "PEGA_AQUÍ_EL_TOKEN_DEL_BOT" && TELEGRAM_CHAT_ID) {
      sendTelegramNotification(data, fechaLocal);
    }
    
    // Devolver respuesta exitosa (formato JSON)
    return ContentService.createTextOutput(JSON.stringify({ "status": "success" }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    // Devolver error si algo falla
    return ContentService.createTextOutput(JSON.stringify({ "status": "error", "message": error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function sendTelegramNotification(data, fecha) {
  try {
    var message = "🆕 *Nueva Solicitud de Reserva* 🎓\n" +
                  "-----------------------------------\n" +
                  "📅 *Fecha:* " + fecha + "\n" +
                  "👤 *Nombre:* " + (data.nombre || "No indicado") + "\n" +
                  "📞 *WhatsApp:* " + (data.telefono || "No indicado") + " [💬 Chatear](https://wa.me/" + (data.telefono || "").replace(/\D/g, "") + ")\n" +
                  "✉️ *Email:* " + (data.email || "No indicado") + "\n" +
                  "🛏️ *Habitación:* " + (data.habitacion || "No indicado") + "\n" +
                  "📚 *Estudios:* " + (data.estudios || "No indicado") + (data.ano_curso ? " (" + data.ano_curso + ")" : "") + "\n" +
                  "⏳ *Duración:* " + (data.meses_alquiler || "No indicado") + "\n" +
                  "💼 *Solvencia:* " + (data.solvencia || "No indicado") + "\n" +
                  "-----------------------------------";
                  
    var payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "text": message,
      "parse_mode": "Markdown",
      "disable_web_page_preview": true
    };
    
    var options = {
      "method": "post",
      "contentType": "application/json",
      "payload": JSON.stringify(payload),
      "muteHttpExceptions": true
    };
    
    UrlFetchApp.fetch("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage", options);
  } catch (err) {
    Logger.log("Error al enviar notificación de Telegram: " + err.toString());
  }
}

// FUNCIÓN DE PRUEBA: Ejecuta esto desde el editor para verificar la conexión y forzar la autorización de Google.
function probarTelegram() {
  Logger.log("Iniciando prueba de Telegram...");
  if (TELEGRAM_BOT_TOKEN === "PEGA_AQUÍ_EL_TOKEN_DEL_BOT" || !TELEGRAM_BOT_TOKEN) {
    Logger.log("Error: Debes configurar tu token de Telegram en la variable TELEGRAM_BOT_TOKEN");
    return;
  }
  var response = UrlFetchApp.fetch("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/getMe");
  Logger.log("Respuesta de Telegram: " + response.getContentText());
}
```


4. Haz clic en el icono del **Disco** (Guardar proyecto) en la barra de herramientas superior del editor de código.

---

## Paso 3: Publicar el Script como Aplicación Web
Para que tu web pueda enviarle datos al script, debes publicarlo de la siguiente manera:
1. Haz clic en el botón azul **Implementar** (o *Deploy*) en la esquina superior derecha ➡️ **Nueva implementación** (*New deployment*).
2. En la ventana que aparece, haz clic en la **Rueda dentada** junto a "Seleccionar tipo" y elige **Aplicación web** (*Web app*).
3. Configura los siguientes campos exactamente así:
   - **Descripción**: `Conexión Formulario Web`
   - **Ejecutar como**: **Tu cuenta** (ej. `sanbasilio18013@gmail.com`)
   - **Quién tiene acceso**: **Cualquiera** (*Anyone*) ⚠️ *(Es muy importante elegir "Cualquiera" para que el formulario web de tu landing pueda escribir los datos)*.
4. Haz clic en **Implementar** (*Deploy*).
5. Si es la primera vez, Google te pedirá que **Autorices el acceso**. Pulsa en *Autorizar acceso*, selecciona tu cuenta de correo, haz clic en *Configuración avanzada* (o *Advanced*) abajo a la izquierda, luego pulsa en *Ir a Proyecto sin título (no seguro)* y finalmente pulsa en **Permitir**.
6. Google te dará una **URL de la aplicación web**. Copia esa URL (debe terminar en `/exec`).

---

## Paso 4: Vincular la URL en tu código local
1. Abre el archivo [script.js](file:///C:/Users/mirro/.gemini/antigravity/scratch/san-basilio-coliving/script.js) de tu proyecto.
2. Busca la línea **246**, donde dice:
   ```javascript
   const GOOGLE_SCRIPT_URL = "[PEGA_AQUÍ_LA_URL_DE_TU_GOOGLE_APPS_SCRIPT]";
   ```
3. Reemplaza todo el texto entre comillas con la URL que acabas de copiar de Google. Debe quedar así:
   ```javascript
   const GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/XXXXXX/exec";
   ```
4. Guarda el archivo.
5. Realiza un `git commit` y un `git push` para subir los cambios a GitHub. ¡Tu formulario ya estará registrando visitas directamente en tu Google Sheet!
