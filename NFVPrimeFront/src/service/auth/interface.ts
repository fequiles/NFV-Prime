export interface ISignInRes {
  accessToken: string;
  refreshToken: string;
}

export interface IJwt {
  id: string;
  name: string;
  username: string;
  holdingId?: string;
  iat: number;
  exp: number;
}
