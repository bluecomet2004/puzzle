import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { UserDashbaord } from './user';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) {}

  get(): Observable<UserDashbaord> {
    return this.http.get<UserDashbaord>('http://127.0.0.1:8000/api/users/');
  }
}
