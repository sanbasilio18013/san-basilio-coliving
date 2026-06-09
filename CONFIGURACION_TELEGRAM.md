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
