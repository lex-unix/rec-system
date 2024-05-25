type ToastData = {
  data: {
    title: string;
    description: string;
  };
};

export const ISSUE_RESOLVED_TOAST_MSG: ToastData = {
  data: {
    title: 'Заявку закрито',
    description: 'Заявку закрито. Дякуємо за ваш відгук.'
  }
};

export const ISSUE_RESOLVED_TOAST_ERROR_MSG: ToastData = {
  data: {
    title: 'Не вдалося закрити заявку',
    description:
      'Наразі не вдалося закрити заявку. Будь ласка, спробуйте пізніше.'
  }
};

export const CHAT_LOADED_TOAST_ERROR_MSG: ToastData = {
  data: {
    title: 'Не вдалося завантажити повідомлення',
    description:
      'Сталася помилка при завантаженні ваших чат-повідомлень. Будь ласка, спробуйте пізніше.'
  }
};

export const ISSUE_LOADED_TOAST_ERROR_MSG: ToastData = {
  data: {
    title: 'Не вдалося завантажити заявку',
    description:
      'Сталася помилка при завантаженні вашої заявки. Будь ласка, спробуйте пізніше.'
  }
};

export const ISSUE_CREATED_TOAST_MSG: ToastData = {
  data: {
    title: 'Заявку сформовано',
    description: 'Очікуйте на відповідь оператора.'
  }
};
