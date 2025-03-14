import type { Messages, Direction, Locale } from '@nuxt/ui-pro'
import { defu } from 'defu'

interface DefineLocaleOptions<M> {
  name: string
  code: string
  dir?: Direction
  messages: M
}

export function defineLocale<M>(options: DefineLocaleOptions<M>): Locale<M> {
  return defu<DefineLocaleOptions<M>, [{ dir: Direction }]>(options, { dir: 'ltr' })
}

export default defineLocale<Messages>({
  name: 'Русский',
  code: 'ru',
  messages: {
    inputMenu: {
      noMatch: 'Совпадений не найдено',
      noData: 'Нет данных',
      create: 'Создать "{label}"'
    },
    calendar: {
      prevYear: 'Предыдущий год',
      nextYear: 'Следующий год',
      prevMonth: 'Предыдущий месяц',
      nextMonth: 'Следующий месяц'
    },
    inputNumber: {
      increment: 'Увеличить',
      decrement: 'Уменьшить'
    },
    commandPalette: {
      placeholder: 'Введите команду или выполните поиск...',
      noMatch: 'Совпадений не найдено',
      noData: 'Нет данных',
      close: 'Закрыть'
    },
    selectMenu: {
      noMatch: 'Совпадений не найдено',
      noData: 'Нет данных',
      create: 'Создать "{label}"',
      search: 'Поиск...'
    },
    toast: {
      close: 'Закрыть'
    },
    carousel: {
      prev: 'Назад',
      next: 'Далее',
      goto: 'Перейти к {slide}'
    },
    modal: {
      close: 'Закрыть'
    },
    slideover: {
      close: 'Закрыть'
    },
    alert: {
      close: 'Закрыть'
    },
    table: {
      noData: 'Нет данных'
    }
  }
})