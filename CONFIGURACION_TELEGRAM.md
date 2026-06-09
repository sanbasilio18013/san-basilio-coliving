# 📢 Configuración del Bot de Telegram para Notificaciones de Reservas

Este documento te guiará paso a paso para configurar un Bot de Telegram gratuito que te enviará una notificación instantánea al móvil cada vez que recibas una nueva solicitud de reserva en la web.

La notificación incluirá todos los datos del candidato (nombre, estudios, etc.) y un **enlace directo para escribirle por WhatsApp con un solo toque**.

---

## Paso 1: Crear el Bot en Telegram
1. Abre tu aplicación de Telegram y busca al usuario oficial **`@BotFather`** (el creador oficial de bots, que tiene un check azul de verificación).
2. Abre un chat con él y pulsa en **Iniciar** (o envía el comando `/start`).
3. Envía el comando `/newbot`.
4. El bot te pedirá un nombre para tu bot. Escribe por ejemplo: `San Basilio Notificaciones`.
5. Después, te pedirá un nombre de usuario (*username*) que debe terminar obligatoriamente en `bot`. Escribe por ejemplo: `sanbasiliocoliving_bot` (si está cogido, prueba con otro número o combinación).
6. ¡Listo! `@BotFather` te enviará un mensaje de éxito con el **token de acceso (HTTP API Token)**. El token tiene un formato similar a esto:
   `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`
   **Copia este token y guárdalo**, lo usaremos en el Paso 3.

---

## Paso 2: Obtener tu `chat_id` personal
Para que el bot sepa a qué chat (o grupo) debe enviar los mensajes, necesitas tu ID único de Telegram:
1. En el buscador de Telegram, busca al usuario **`@GetChatID_Bot`** o **`@userinfobot`**.
2. Inicia el chat con él.
3. Te responderá inmediatamente con tu información, donde verás un campo llamado **`Id`** (es un número de 9 o 10 dígitos, por ejemplo: `987654321`).
4. **Copia este número**.

> [!TIP]
> **¿Quieres recibir los avisos en un grupo de Telegram? (Para compartirlo con socios)**
> 1. Crea un grupo en Telegram y añade a tu bot (el que creaste en el Paso 1).
> 2. Añade también al bot `@GetChatID_Bot` al grupo de forma temporal.
> 3. El bot imprimirá en el chat el ID del grupo (suele empezar por un guion `-`, por ejemplo: `-1001234567890`).
> 4. Copia ese ID con el signo `-` incluido, y luego puedes expulsar a `@GetChatID_Bot` del grupo.

---

## Paso 3: Configurar el script en tu Hoja de Cálculo
Ahora uniremos el Bot de Telegram con el script de Google Sheets:
1. Abre tu Hoja de cálculo de Google.
2. Ve al menú **Extensiones** ➡️ **Apps Script**.
3. Reemplaza el código existente en `Código.gs` con la versión actualizada (que tienes en la guía [CONFIGURACION_GOOGLE_SHEETS.md](file:///C:/Users/mirro/.gemini/antigravity/scratch/san-basilio-coliving/CONFIGURACION_GOOGLE_SHEETS.md) o abajo).
4. En las primeras líneas del código, rellena tus dos variables con el token y el ID obtenidos:
   ```javascript
   var TELEGRAM_BOT_TOKEN = "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ"; // Pon tu token aquí
   var TELEGRAM_CHAT_ID = "987654321"; // Pon tu chat_id (o ID de grupo) aquí
   ```
5. Haz clic en el icono del **Disco** (Guardar proyecto).
6. **MUY IMPORTANTE**: Para que Google aplique el nuevo código de notificaciones, debes realizar una **Nueva versión de la implementación**:
   - Haz clic en **Implementar** ➡️ **Administrar implementaciones** (*Manage deployments*).
   - Haz clic en el icono del **Lápiz** (Editar) en la implementación actual.
   - En el menú desplegable "Versión", selecciona **Nueva versión** (*New version*).
   - Haz clic en **Implementar** (*Deploy*).

---

## Paso 4: Iniciar el chat con el bot
Antes de que tu bot pueda enviarte mensajes por primera vez, Telegram requiere que des tu consentimiento:
1. Busca el nombre de usuario de tu bot en Telegram (ej: `@sanbasiliocoliving_bot`).
2. Abre un chat con él y pulsa en **Iniciar** (o envía `/start`).
3. *(Si es un grupo, asegúrate de que el bot está dentro del grupo y tiene permisos de escritura).*

¡Eso es todo! La próxima vez que alguien rellene el formulario de tu página web:
1. Se guardarán los datos en la hoja de cálculo.
2. Tu bot de Telegram te enviará un mensaje al instante.
3. El mensaje tendrá un formato limpio y un botón para abrir directamente un chat de WhatsApp con el número del candidato sin tener que guardarlo en la agenda.

---

## 🛠️ Resolución de Problemas: Error de Permisos (UrlFetchApp)

Si al ejecutar el script o enviar el formulario ves un error como:
`Exception: You do not have permission to call UrlFetchApp.fetch. Required permissions: https://www.googleapis.com/auth/script.external_request`

Sigue estos pasos para solucionarlo:

### 1. Forzar la Autorización desde el Editor
A veces, Google Apps Script no muestra el diálogo de autorización inicial si el código problemático está dentro de un bloque `try-catch`. Para forzarlo:

1. En tu editor de Apps Script, añade esta función temporal al **final** de tu archivo `Código.gs`:
   ```javascript
   function probarTelegram() {
     Logger.log("Iniciando prueba de Telegram...");
     var response = UrlFetchApp.fetch("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/getMe");
     Logger.log("Respuesta de Telegram: " + response.getContentText());
   }
   ```
2. Haz clic en el **Disco** (Guardar).
3. En la barra de herramientas superior, selecciona la función `probarTelegram` en el desplegable y haz clic en **Ejecutar** (Run).
4. Google **bloqueará la ejecución** y mostrará una ventana flotante de **"Autorización requerida"** (Authorization Required).
5. Haz clic en **Revisar permisos** (Review permissions).
6. Selecciona tu cuenta de Google.
7. Si te sale un aviso de "Google no ha verificado esta aplicación", haz clic en **Configuración avanzada** (abajo a la izquierda) y luego en **Ir a Proyecto sin título (no seguro)**.
8. Haz clic en **Permitir** (Allow).
9. La función se ejecutará y deberías ver en el registro: `"Respuesta de Telegram: {"ok":true,...}"`. Esto significa que tanto los permisos como tu token son correctos.

### 2. Verificar el archivo de manifiesto (`appsscript.json`)
Si al ejecutar `probarTelegram` sigue dando el error de permisos sin mostrar la ventana de autorización:

1. Ve a la **Configuración del proyecto** (icono de engranaje ⚙️ en la barra lateral izquierda de Apps Script).
2. Marca la casilla **"Mostrar el archivo de manifiesto 'appsscript.json' en el editor"**.
3. Vuelve al **Editor** (icono de código `<>`) y haz clic en el archivo `appsscript.json` que ahora aparece en la lista.
4. Asegúrate de que **no** haya una sección llamada `"oauthScopes"` que esté limitando los permisos del script. Si la hay, añade `"https://www.googleapis.com/auth/script.external_request"` a la lista, o directamente elimina la sección `"oauthScopes"` entera para que Google detecte automáticamente los permisos que tu código necesita.

### 3. Crear una nueva versión de la implementación
Una vez que `probarTelegram` funcione correctamente, debes **actualizar la versión pública de la aplicación web** para que herede estos permisos autorizados:

1. Haz clic en **Implementar** ➡️ **Administrar implementaciones** (*Manage deployments*).
2. Haz clic en el icono del **Lápiz** (Editar) en tu implementación activa.
3. En el menú desplegable "Versión", selecciona **Nueva versión** (*New version*).
4. Haz clic en **Implementar** (*Deploy*).

