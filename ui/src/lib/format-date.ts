export function formatTime(date: Date) {
  return new Intl.DateTimeFormat('default', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true
  }).format(date);
}
