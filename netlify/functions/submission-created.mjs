// Auto-reply to website enquiries. Netlify runs this automatically for every verified form submission.
// Needs two environment variables in Netlify (Site configuration → Environment variables):
//   SMTP_USER = sales@polymerpaints.com
//   SMTP_PASS = the Google App Password of that mailbox (16 characters, no spaces)
// If they are missing the function does nothing, so the forms keep working as before.
import nodemailer from 'nodemailer';

const FORMS = ['contact', 'sample', 'documents', 'distributor', 'contact-ru', 'contact-es'];
const WA = ['+86 158 2472 9376', '+86 188 5021 3808'];

const COPY = {
  en: {
    subject: 'We have received your enquiry | POLYMER Powder Coatings',
    hi: n => `Dear ${n},`,
    body: ['Thank you for contacting POLYMER. Our sales and technical team has received your enquiry and will reply within one working day (Monday to Saturday, UTC+8).',
           'To speed things up, you can reply to this email with photos of the part, your colour reference (RAL code or a photo of the sample), the substrate and pretreatment, and the expected volume.'],
    yours: 'Your message', sign: 'Kind regards,<br>POLYMER Sales Team<br>Fujian Polymer Industry &amp; Trade Co., Ltd.',
    more: 'Useful while you wait', links: [['System selector', 'https://polymerpaints.com/selector/'], ['Colours & finishes', 'https://polymerpaints.com/finishes/'], ['FAQ', 'https://polymerpaints.com/faq/']],
    note: 'This is an automatic confirmation. Please do not share passwords or payment details by email.'
  },
  ru: {
    subject: 'Мы получили ваш запрос | POLYMER Powder Coatings',
    hi: n => `Здравствуйте, ${n}!`,
    body: ['Спасибо за обращение в POLYMER. Наша команда получила ваш запрос и ответит в течение рабочего дня (пн–сб, UTC+8). Мы отвечаем на английском языке.',
           'Чтобы ускорить подбор, ответьте на это письмо и приложите фото детали, цвет (код RAL или фото образца), материал основы и подготовку поверхности, а также ожидаемый объём.'],
    yours: 'Ваше сообщение', sign: 'С уважением,<br>отдел продаж POLYMER<br>Fujian Polymer Industry &amp; Trade Co., Ltd.',
    more: 'Полезные материалы', links: [['Русская страница', 'https://polymerpaints.com/ru/'], ['FAQ (EN)', 'https://polymerpaints.com/faq/']],
    note: 'Это автоматическое подтверждение. Не отправляйте пароли и платёжные данные по электронной почте.'
  },
  es: {
    subject: 'Hemos recibido su consulta | POLYMER Powder Coatings',
    hi: n => `Estimado/a ${n}:`,
    body: ['Gracias por contactar a POLYMER. Nuestro equipo recibió su consulta y responderá en un día hábil (de lunes a sábado, UTC+8). Respondemos en inglés.',
           'Para agilizar, puede responder a este correo con fotos de la pieza, su referencia de color (código RAL o foto de la muestra), el sustrato y el pretratamiento, y el volumen previsto.'],
    yours: 'Su mensaje', sign: 'Saludos cordiales,<br>Equipo de ventas POLYMER<br>Fujian Polymer Industry &amp; Trade Co., Ltd.',
    more: 'Información útil', links: [['Página en español', 'https://polymerpaints.com/es/'], ['FAQ (EN)', 'https://polymerpaints.com/faq/']],
    note: 'Este es un acuse de recibo automático. No envíe contraseñas ni datos de pago por correo.'
  }
};

const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const okEmail = e => typeof e === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e) && e.length < 200;

export function buildMail(payload) {
  const d = payload.data || {};
  const form = payload.form_name || d['form-name'] || '';
  const lang = form.endsWith('-ru') ? 'ru' : form.endsWith('-es') ? 'es' : 'en';
  const c = COPY[lang];
  const name = (d.name || '').toString().trim().slice(0, 80) || (lang === 'ru' ? 'коллега' : lang === 'es' ? 'cliente' : 'customer');
  const msg = (d.message || '').toString().slice(0, 4000);
  const rows = [['Company', d.company], ['Country', d.country], ['Role', d.role], ['System', d.system], ['Finish', d.finish]].filter(r => r[1]);
  const html = `<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.6;color:#141618;max-width:600px">
<div style="background:#121416;padding:20px 24px"><span style="color:#fff;font-weight:700;letter-spacing:4px;font-size:16px">POLYMER</span> <span style="color:#9a9fa5;font-size:11px;letter-spacing:2px">POWDER COATINGS</span></div>
<div style="padding:24px;border:1px solid #dcdfe1;border-top:0">
<p>${esc(c.hi(name))}</p>${c.body.map(p => `<p>${esc(p)}</p>`).join('')}
${msg ? `<p style="margin-top:22px;font-size:12px;letter-spacing:1px;color:#6e7278;text-transform:uppercase">${esc(c.yours)}</p><div style="background:#f2f3f3;padding:14px 16px;white-space:pre-wrap">${esc(msg)}</div>` : ''}
${rows.length ? `<table style="margin-top:10px;font-size:13px;color:#3d4146">${rows.map(r => `<tr><td style="padding:2px 14px 2px 0;color:#6e7278">${esc(r[0])}</td><td>${esc(r[1])}</td></tr>`).join('')}</table>` : ''}
<p style="margin-top:22px">${c.sign}</p>
<p style="font-size:13px;color:#3d4146">sales@polymerpaints.com · +86 596 2600611<br>WhatsApp ${WA.join(' · ')}<br><a href="https://polymerpaints.com/" style="color:#c8231a">polymerpaints.com</a></p>
<p style="margin-top:18px;font-size:12px;letter-spacing:1px;color:#6e7278;text-transform:uppercase">${esc(c.more)}</p>
<p style="font-size:13px">${c.links.map(l => `<a href="${l[1]}" style="color:#c8231a">${esc(l[0])}</a>`).join(' · ')}</p>
<p style="margin-top:18px;font-size:11px;color:#9a9fa5">${esc(c.note)}</p></div></div>`;
  const text = [c.hi(name), '', ...c.body, '', msg ? `${c.yours}:\n${msg}\n` : '', 'POLYMER Sales Team', 'sales@polymerpaints.com · +86 596 2600611', `WhatsApp ${WA.join(' · ')}`, 'https://polymerpaints.com/', '', c.note].join('\n');
  return { lang, form, to: d.email, subject: c.subject, html, text };
}

export const handler = async (event) => {
  try {
    const { payload } = JSON.parse(event.body || '{}');
    if (!payload) return { statusCode: 200, body: 'no payload' };
    const d = payload.data || {};
    const form = payload.form_name || d['form-name'] || '';
    if (!FORMS.includes(form)) return { statusCode: 200, body: 'form ignored' };
    if (d['bot-field']) return { statusCode: 200, body: 'bot ignored' };
    if (!okEmail(d.email)) return { statusCode: 200, body: 'no valid email' };
    const user = process.env.SMTP_USER, pass = (process.env.SMTP_PASS || '').replace(/\s+/g, '');
    if (!user || !pass) { console.log('auto-reply skipped: SMTP_USER / SMTP_PASS not set'); return { statusCode: 200, body: 'not configured' }; }
    const m = buildMail(payload);
    const tx = nodemailer.createTransport({ host: 'smtp.gmail.com', port: 465, secure: true, auth: { user, pass } });
    await tx.sendMail({ from: `"POLYMER Sales" <${user}>`, replyTo: user, to: m.to, subject: m.subject, text: m.text, html: m.html });
    console.log(`auto-reply sent (${m.form}, ${m.lang})`);
    return { statusCode: 200, body: 'sent' };
  } catch (e) {
    console.log('auto-reply error:', e && e.message);
    return { statusCode: 200, body: 'error logged' }; // never block the submission
  }
};
