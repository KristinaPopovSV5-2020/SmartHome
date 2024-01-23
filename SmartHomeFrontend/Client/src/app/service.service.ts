import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

import { Socket } from 'ngx-socket-io';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ServiceService {

  constructor(private http: HttpClient, private socket: Socket) { }

  getMessage() {
    return this.socket.fromEvent('data').pipe(map((data: any) => data.msg));
  }



  getDevices() : Observable<any> {
    return this.http.get<any>(environment.apiHost + 'aggregate_query');
}
}
