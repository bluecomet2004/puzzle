import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HistoryDashboard } from './history';
import { HistoryMessage } from './history';

@Injectable({
  providedIn: 'root'
})
export class HistoryService {
  constructor(private http: HttpClient) {}

  get(page: number = 1, limit: number = 10, search: string = ''): Observable<HistoryDashboard> {
    return this.http.get<HistoryDashboard>(`http://127.0.0.1:8000/api/history/?page=${page}&limit=${limit}&search=${search}`);
  }

  delete(id: string): Observable<HistoryMessage> {
    return this.http.delete<HistoryMessage>(`http://127.0.0.1:8000/api/history/?id=${id}`);
  }
}
