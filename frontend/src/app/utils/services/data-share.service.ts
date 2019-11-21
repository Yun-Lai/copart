import { Injectable } from '@angular/core';
import { BehaviorSubject } from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class DataShareService {

  private filterWordContainer = new BehaviorSubject('');
  currentFilterWord =  this.filterWordContainer.asObservable();

  constructor() { }

  setFilterWord(filterWord: string) {
    this.filterWordContainer.next(filterWord)
  }
}
