type ToastData = {
  data: {
    title: string;
    description: string;
  };
};

export const ISSUE_RESOLVED_TOAST_MSG: ToastData = {
  data: {
    title: 'Issue resolved',
    description: 'Issue is now closed. Thank you for your feedback'
  }
};

export const ISSUE_RESOLVED_TOAST_ERROR_MSG: ToastData = {
  data: {
    title: 'Failed to resolve the issue',
    description:
      "We couldn't resolve the issue at the moment. Please, try again later."
  }
};

export const CHAT_LOADED_TOAST_ERROR_MSG: ToastData = {
  data: {
    title: 'Failed to load messages',
    description:
      'There was an error loading your chat messages. Please, try again later.'
  }
};

export const ISSUE_LOADED_TOAST_ERROR_MSG: ToastData = {
  data: {
    title: 'Failed to issue',
    description:
      'There was an error loading your issue. Please try again later.'
  }
};
