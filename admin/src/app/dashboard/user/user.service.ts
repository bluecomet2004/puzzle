import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { UserDashbaord, Message } from './user';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) {}

  get(page: number = 1, limit: number = 10, search: string = ''): Observable<UserDashbaord> {
    return this.http.get<UserDashbaord>(`http://127.0.0.1:8000/api/users/?page=${page}&limit=${limit}&search=${search}`);
  }

  update(id: string, name: string): Observable<Message> {
    return this.http.put<Message>(`http://127.0.0.1:8000/api/users/?id=${id}`, {name});
  }

  delete(id: string): Observable<Message> {
    return this.http.delete<Message>(`http://127.0.0.1:8000/api/users/?id=${id}`);
  }
}
