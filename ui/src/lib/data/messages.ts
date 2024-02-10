import { faker } from '@faker-js/faker';

const MAX_MESSAGES = 40;
const MESSAGE_INTERVAL = 2;

type Message = {
  text: string;
  me: boolean;
  date: Date;
};

export const messages: Message[] = [];

for (let i = 0; i < MAX_MESSAGES; ++i) {
  const text = faker.lorem.sentences({ min: 1, max: 3 });
  const me = i % 2 === 0;
  const date = new Date();
  date.setMinutes(date.getMinutes() + MESSAGE_INTERVAL * (i + 1));

  messages.push({ text, me, date });
}
