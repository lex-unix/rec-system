export type User = {
  id: number;
  fullName: string;
  email: string;
};

export type Issue = {
  id: number;
  subject: string;
  description: string;
  type: string;
  userId: number;
};
