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

  dmsChangeDevice(code: string): Observable<any> {
    return this.http.post<any>(environment.apiHost + 'dms_change_state', {'code': code});
  }

  birChangeDevice(code: string): Observable<any> {
    return this.http.post<any>(environment.apiHost + 'bir_change_state', {'code': code});
  }

  b4sdChangeDevice(): Observable<any> {
    return this.http.post<any>(environment.apiHost + 'b4sd_change_state', {
      "intermittently": false,
      "turnOn": true
  });
  }

  setAlarm(time: string): Observable<any> {
    return this.http.post<any>(environment.apiHost + 'set_alarm', {'value': time});
  }

  cancelAlarm(): Observable<any> {
    return this.http.post<any>(environment.apiHost + 'cancel_alarm', {'value': false});
  }
}
