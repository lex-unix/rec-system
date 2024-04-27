import type { issueTypes } from './data/issue-types';
import type { issueStatus } from './issues';

export type User = {
  id: number;
  full_name: string;
  email: string;
};

export type IssueType = keyof typeof issueTypes;
export type IssueStatus = keyof typeof issueStatus;

export type Issue = {
  id: number;
  subject: string;
  description: string;
  status: IssueStatus;
  type: IssueType;
  user_id: number;
  operator: Operator;
};

export type SocketData = {
  message: string;
  user_id: number;
  created_at: Date;
};

export type Chat = {
  id: number;
  issueId: number;
  created_at: string;
  messages: Message[];
};

export type Message = {
  id: number;
  chat_id: number;
  sender_id: number;
  created_at: string;
  content: string;
};

export type Operator = {
  id: number;
  full_name: string;
  rating: number;
  availability: boolean;
  resolved_issues: number;
};
