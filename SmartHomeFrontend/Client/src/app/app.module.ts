import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MaterialModule } from 'src/infrastructure/material.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { HistoryComponent } from './history/history.component';
import { HomeComponent } from './home/home.component';
import { SharedModule } from './shared/shared.module';
import { HttpClientModule } from '@angular/common/http';

import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { AlarmDialogComponent } from './alarm-dialog/alarm-dialog.component';
import { DmsDialogComponent } from './dms-dialog/dms-dialog.component';
import { BirDialogComponent } from './bir-dialog/bir-dialog.component';

const config: SocketIoConfig = { url: 'http://127.0.0.1:5000', options: {} };

@NgModule({
  declarations: [
    AppComponent,
    ToolbarComponent,
    HistoryComponent,
    HomeComponent,
    AlarmDialogComponent,
    DmsDialogComponent,
    BirDialogComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialModule,
    BrowserAnimationsModule,
    SharedModule,
    HttpClientModule,
    SocketIoModule.forRoot(config),
  ],
  bootstrap: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule { }
