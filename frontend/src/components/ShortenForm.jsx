import React from 'react'
import { useState } from 'react'

const ShortenForm = ({onSubmit, isSubmitting}) => {
    const [originalUrl, setOriginalUrl ] = useState('')
    const [customCode, setCustomCode] = useState('')
    const [showCustom, setShowCustom] = useState('false')
    const [formError, setFormError] = useState(false)

    const handleSubmit = async(e)=>{
        if(!originalUrl.trim()){
            setFormError("Please paste link first")
        }

        try {
            await onSubmit({originalUrl : originalUrl.trim(), customCode :customCode.trim()})
            setOriginalUrl('')
            setCustomCode('') 
        } catch (error) {
            setFormError(error.message | "Something went wrong")
        }
    }


  return (
    <form className="shorten-form" onSubmit={handleSubmit}>
      <div className="shorten-form__row">
        <input
          type="text"
          inputMode="url"
          className="shorten-form__input"
          placeholder="Paste a long link — https://example.com/…"
          value={originalUrl}
          onChange={(e) => setOriginalUrl(e.target.value)}
          disabled={isSubmitting}
          aria-label="Long URL to shorten"
        />
        <button type="submit" className="shorten-form__submit" disabled={isSubmitting}>
          {isSubmitting ? "Snipping…" : "Snip it"}
        </button>
      </div>

      <button
        type="button"
        className="shorten-form__toggle"
        onClick={() => setShowCustom((v) => !v)}
      >
        {showCustom ? "Hide custom alias" : "Use a custom alias"}
      </button>

      {showCustom && (
        <input
          type="text"
          className="shorten-form__input shorten-form__input--custom"
          placeholder="my-alias (letters, numbers, - and _ only)"
          value={customCode}
          onChange={(e) => setCustomCode(e.target.value)}
          disabled={isSubmitting}
          aria-label="Custom short code"
        />
      )}

      {formError && <p className="shorten-form__error">{formError}</p>}
    </form>
  );
}

export default ShortenForm
