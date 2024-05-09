import type { User } from './types';
import { writable } from 'svelte/store';

export const user = writable<User | undefined>(undefined);

export const useChatbot = writable(true);
